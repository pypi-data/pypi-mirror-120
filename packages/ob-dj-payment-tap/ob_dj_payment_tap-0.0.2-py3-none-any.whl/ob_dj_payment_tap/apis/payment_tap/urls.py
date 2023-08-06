from rest_framework.routers import SimpleRouter

from ob_dj_payment_tap.apis.payment_tap.views import TapPaymentViewSet

app_name = "payment_tap"

router = SimpleRouter(trailing_slash=False)
router.register(r"gateway_tap", TapPaymentViewSet)

urlpatterns = router.urls
