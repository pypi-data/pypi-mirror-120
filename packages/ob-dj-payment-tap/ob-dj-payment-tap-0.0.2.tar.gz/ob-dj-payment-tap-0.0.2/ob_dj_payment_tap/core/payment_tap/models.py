import logging
import typing

from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_cryptography.fields import encrypt

from ob_dj_payment_tap.core.payment_tap.managers import (
    TapConfigManager,
    TapTransactionManager,
)
from ob_dj_payment_tap.core.payment_tap.utils import TapAPI, TapChallengeException

logger = logging.getLogger(__name__)


class TapConfig(models.Model):
    """TAPConfig represent configuration to maintain for single or multi retail configuration"""

    publishable_api_key = models.CharField(max_length=400, unique=True)
    # TODO: Add external identifier
    secret = encrypt(models.CharField(max_length=3000))

    objects = TapConfigManager()

    class Meta:
        verbose_name = _("TAP Config")


class TapTransaction(models.Model):
    """ TapTransaction represent every attempt for a charge; a record will be created in
    TapTransaction to capture the transaction and callback confirmation. A transaction
    will be
    """

    class Status(models.TextChoices):
        INITIATED = "INITIATED"
        IN_PROGRESS = "IN_PROGRESS"
        ABANDONED = "ABANDONED"
        CANCELLED = "CANCELLED"
        FAILED = "FAILED"
        DECLINED = "DECLINED"
        RESTRICTED = "RESTRICTED"
        CAPTURED = "CAPTURED"
        VOID = "VOID"
        TIMEDOUT = "TIMEDOUT"
        UNKNOWN = "UNKNOWN"

    class Sources(models.TextChoices):
        CREDIT_CARD = "src_card", _("Credit Card")
        KNET = "src_kw.knet", _("KNet")

    config = models.ForeignKey(
        TapConfig, on_delete=models.CASCADE, related_name="transactions"
    )
    status = models.CharField(max_length=100, choices=Status.choices)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        help_text=_(
            "Captured the User ID for both registered "
            "users and Guests (Every guest user has a user_id assigned by device_id)"
        ),
    )
    langid = models.CharField(
        max_length=10,
        help_text=_(
            "Capture language for debugging & analytical only purposes (ARA for Arabic & ENG for English)"
        ),
    )
    amount = models.DecimalField(max_digits=20, decimal_places=3,)
    result = models.CharField(
        max_length=100, help_text=_("Status response from TAP gateway")
    )
    # payment details
    payment_url = models.CharField(
        max_length=250, help_text=_("Captures generated URL for user payment")
    )
    charge_id = models.CharField(
        max_length=250,
        help_text=_("Charge ID returned from TAP"),
        unique=True,
        db_index=True,
    )
    init_response = models.JSONField(
        help_text=_("Response received when initiating the payment"),
        null=True,
        blank=True,
    )
    callback_response = models.JSONField(
        help_text=_("Callback response received after the payment is done"),
        null=True,
        blank=True,
    )
    # security
    encrypt_key = models.BinaryField(max_length=200, null=True, blank=True)
    # audit fields
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        help_text=_("Datetime when payment was initiated"),
    )
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True,)

    objects = TapTransactionManager()

    class Meta:
        verbose_name = _("TAP Transaction")

    @property
    def paid(self):
        return self.status == self.Status.CAPTURED

    def update_transaction_status(
        self, response: typing.Dict = None
    ) -> typing.NoReturn:
        if not response:
            response = TapAPI(tap_config=self.config).get_charge_status(
                charge_id=self.charge_id
            )
        self.update_from_payload(payload=response)

    def update_from_payload(self, payload: typing.Dict) -> typing.NoReturn:
        """ when receiving a call from TAP and marking transaction
        :return:
        """
        logger.info("Validate transaction salt")
        # TODO: Add validation; only initiated transactions can be updated
        logger.info(f"Mark TAP Transaction started for charge ID {self.charge_id}")
        logger.info(f"Payload value: {payload}")
        self.result = payload["status"]
        self.callback_response = payload
        self.status = payload["status"]
        # save
        self.save()
        logger.info(f"Mark TAP Transaction finished for charge ID {self.charge_id}")

    def validate_challenge(
        self, data: typing.Text, raise_exception: bool = False
    ) -> bool:
        try:
            cipher = Fernet(self.encrypt_key)
            user_id = self.user.id.__str__().encode()
            decrypted_challenge = cipher.decrypt(data.encode("utf-8"))
            logger.debug(
                f"Solving challenge for charge_id={self.charge_id} "
                f"<UserID:{user_id}>"
                f"<DecryptedChallenge:{decrypted_challenge}>"
            )
            if cipher.decrypt(data.encode("utf-8")) != user_id:
                raise TapChallengeException
            return True
        except TapChallengeException:
            if raise_exception:
                raise
            return False

    # TODO: What is the use case of reference_id?
    @property
    def reference_id(self):
        reference = self.callback_response.get("reference")
        return reference.get("payment") if reference else ""

    # TODO: What is the use case of source?
    @property
    def source(self):
        source = self.init_response.get("source")
        return source.get("id") if source else ""
