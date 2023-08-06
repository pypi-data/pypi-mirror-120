import typing

from django.conf import settings
from django.db import models

from ob_dj_payment_tap.core.payment_tap.utils import TapAPI


class TapConfigManager(models.Manager):
    pass


class TapTransactionManager(models.Manager):
    def create(self, *args: typing.Any, **kwargs: typing.Any):
        # If config not found in kwargs TapTransaction will
        # look for a settings config and create/or get the
        # TapConfig related
        if (
            not kwargs.get("config")
            and hasattr(settings, "TAP_CONFIG_SECRET")
            and hasattr(settings, "TAP_CONFIG_API_KEY")
        ):
            # Creates default entry to TapConfig if Settings found
            (
                config,
                created,
            ) = self.model.config.field.related_model.objects.get_or_create(
                publishable_api_key=settings.TAP_CONFIG_API_KEY,
                defaults={"secret": settings.TAP_CONFIG_SECRET},
            )
            kwargs["config"] = config

        if not kwargs.get("config"):
            raise ValueError(
                "TAP Secret is missing from settings and/or not defined in TAPConfig Table."
            )

        if (
            "source" not in kwargs
            or kwargs.get("source") not in self.model.Sources.values
        ):
            raise ValueError("Invalid source value.")

        source = kwargs.pop("source")
        tap_kwargs = {}
        if "config" in kwargs:
            tap_kwargs.update(tap_config=kwargs["config"])

        tap_initiate = TapAPI(**tap_kwargs).initiate(
            source=source,
            amount=kwargs.get("amount"),
            user=kwargs.get("user"),
            # TODO: param currency
            currency_code="KWD",
        )
        kwargs["charge_id"] = tap_initiate.charge_id
        kwargs["payment_url"] = tap_initiate.payment_url
        kwargs["init_response"] = tap_initiate.response
        kwargs["status"] = tap_initiate.response["status"]
        kwargs["encrypt_key"] = tap_initiate.encrypt_key
        return super().create(**kwargs)
