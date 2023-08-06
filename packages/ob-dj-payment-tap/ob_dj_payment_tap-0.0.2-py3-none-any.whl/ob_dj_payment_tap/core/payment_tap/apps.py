from django.apps import AppConfig
from django.core.checks import register
from django.utils.translation import gettext_lazy as _

from ob_dj_payment_tap.core.payment_tap import settings_validation


class PaymentTapConfig(AppConfig):
    name = "ob_dj_payment_tap.core.payment_tap"
    verbose_name = _("Tap Payment")

    def ready(self):
        register(settings_validation.required_settings)
        register(settings_validation.required_dependencies)
        register(settings_validation.required_installed_apps)
