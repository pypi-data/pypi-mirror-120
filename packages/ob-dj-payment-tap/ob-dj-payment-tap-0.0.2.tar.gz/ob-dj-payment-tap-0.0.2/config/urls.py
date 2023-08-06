from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"payment_tap/", include("ob_dj_payment_tap.apis.payment_tap.urls"),),
]
