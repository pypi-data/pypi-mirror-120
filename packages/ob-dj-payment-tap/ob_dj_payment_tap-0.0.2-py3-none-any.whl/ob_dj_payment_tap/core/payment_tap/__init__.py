import typing

from config import settings

default_app_config = "ob_dj_payment_tap.core.payment_tap.apps.PaymentTapConfig"


def setting_or_default(setting: typing.Text) -> typing.Any:
    """Returns default values for settings if not found"""
    settings_defaults = {
        "PAYMENT_TAP_DEFAULT_MAX_DIGITS": 20,
        "PAYMENT_TAP_DEFAULT_DECIMAL_PLACES": 3,
    }
    try:
        return getattr(settings, setting)
    except AttributeError:
        return settings_defaults[setting]
