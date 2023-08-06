from setuptools import setup

# version = "0.0.1"

setup(
    install_requires=["django", "djangorestframework", "django_cryptography"],
    packages=[
        "ob_dj_payment_tap.apis",
        "ob_dj_payment_tap.apis.payment_tap",
        "ob_dj_payment_tap.core",
        "ob_dj_payment_tap.core.payment_tap",
        "ob_dj_payment_tap.core.payment_tap.migrations",
    ],
    tests_require=["pytest"],
    use_scm_version={"write_to": "version.py",},
    setup_requires=["setuptools_scm"],
)
