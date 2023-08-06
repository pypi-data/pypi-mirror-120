from django.contrib import admin

from ob_dj_payment_tap.core.payment_tap.models import TapConfig, TapTransaction


class TapConfigAdmin(admin.ModelAdmin):
    """ TapConfigAdmin
    """

    model = TapConfig


class TapTransactionAdmin(admin.ModelAdmin):
    """ TapTransactionAdmin
    """

    model = TapTransaction


admin.site.register(TapConfig, TapConfigAdmin)
admin.site.register(TapTransaction, TapTransactionAdmin)
