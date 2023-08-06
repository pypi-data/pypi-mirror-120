import json
import logging
import typing
from decimal import Decimal

import requests
from cryptography.fernet import Fernet
from django.core.serializers.json import DjangoJSONEncoder
from requests import HTTPError
from rest_framework import status
from rest_framework.reverse import reverse

from ob_dj_payment_tap.core.payment_tap import setting_or_default

if typing.TYPE_CHECKING:
    from ob_dj_payment_tap.core.payment_tap.models import TapConfig

logger = logging.getLogger(__name__)


class TapInitiateResponse(object):
    def __init__(
        self,
        charge_id: typing.Text,
        payment_url: typing.Text,
        encrypt_key: typing.Text,
        response: typing.Dict,
    ):
        self.charge_id = charge_id
        self.payment_url = payment_url
        self.encrypt_key = encrypt_key
        self.response = response


class TapChallengeException(Exception):
    pass


class TapException(Exception):
    pass


class TapAPI(object):
    """TAPApi class for managing calls and interaction with TAP APIs"""

    tap_config = None
    redirect_url = None
    host = "https://api.tap.company"

    def __init__(self, tap_config: "TapConfig" = None):
        # TODO: use TAP_CONFIG or settings
        # if not tap_config:
        #     pass
        self.tap_config = tap_config

    def _make_request(
        self, payload: typing.Dict, url: typing.Text = None, method: typing.Text = None
    ) -> typing.Dict:
        url = url or "/v2/charges/"
        method = method or "POST"
        tap_secret_key = self.tap_config.secret
        headers = {
            "authorization": f"Bearer {tap_secret_key}",
            "content-type": "application/json",
            "cache-control": "no-cache",
        }
        payload = json.dumps(payload, cls=DjangoJSONEncoder)
        response = requests.request(
            url=f"{self.host}{url}", method=method, data=payload, headers=headers
        )

        try:
            response.raise_for_status()
        except HTTPError as ex:
            if response.status_code == status.HTTP_400_BAD_REQUEST:
                # Includes the 400 error payload
                raise HTTPError(
                    f"{ex.__str__()}\n{response.json().__str__()}", response=response
                )
            raise

        return response.json()

    def get_charge_status(self, charge_id: typing.Text) -> typing.Dict:
        return self._make_request(
            payload={}, url=f"/v2/charges/{charge_id}", method="GET"
        )

    def initiate(
        self,
        source: typing.Text,
        amount: Decimal,
        # TODO: Define type for user without importing user
        user,
        currency_code: typing.Text,
    ) -> TapInitiateResponse:

        # Once the Payment processed, Customer will be redirected to this url
        # in our case we will redirect him/her to TapTransaction details
        # TODO: Automatically define the returned url based on TAP_CONFIG or settings
        redirect_uri = f"{setting_or_default('TAP_KNET_REDIRECT_URI')}"
        callback_uri = f"{setting_or_default('TAP_KNET_CALLBACK_URI')}"

        redirect_path = reverse(f"payment_tap:taptransaction-get")
        callback_path = reverse(f"payment_tap:taptransaction-callback")
        encrypt_key = Fernet.generate_key()
        cipher = Fernet(encrypt_key)
        challenge = cipher.encrypt(user.id.__str__().encode()).decode("utf-8")
        redirect_url = f"{redirect_uri}{redirect_path}?challenge={challenge}"
        callback_url = f"{callback_uri}{callback_path}"

        payload = {
            # TODO: Formatter as settings/config
            "amount": "%.3f" % amount,  # to respect amount format
            # TODO: Currency config should be global on org level?
            "currency": currency_code,
            "source": {"id": source},
            "customer": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
            "post": {"url": callback_url},
            "redirect": {"url": redirect_url},
        }
        response = self._make_request(payload=payload)
        payment_url = response.get("transaction").get("url")
        charge_id = response.get("id")
        if not payment_url or not charge_id:
            # TODO: How does this issue occur and is this the best way to handle it?
            logger.error(
                f"Failed to create charge request no payment_url or charge_id returned."
            )
            raise TapException(payload)

        return TapInitiateResponse(
            charge_id=charge_id,
            payment_url=payment_url,
            encrypt_key=encrypt_key,
            response=response,
        )
