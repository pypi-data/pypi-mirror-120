from django.apps import apps
from django.conf import settings
from django.core.checks import Error

REQUIRED_INSTALLED_APPS = [
    "rest_framework",
]


def required_dependencies(app_configs, **kwargs):
    return []


def required_installed_apps(app_configs, **kwargs):
    return [
        Error(f"{app} is required in INSTALLED_APPS")
        for app in REQUIRED_INSTALLED_APPS
        if not apps.is_installed(app)
    ]


def required_settings(app_configs, **kwargs):
    errors = []
    if not getattr(settings, "TAP_KNET_REDIRECT_URI", None):
        errors.append(Error(f"TAP_KNET_REDIRECT_URI setting is required"))
    if not getattr(settings, "TAP_KNET_CALLBACK_URI", None):
        errors.append(Error(f"TAP_KNET_CALLBACK_URI setting is required"))
    return errors
