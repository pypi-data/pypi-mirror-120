from celery import shared_task
from django.db.models import Q

from ob_dj_payment_tap.core.payment_tap.models import TapTransaction


@shared_task
def mark_tap_transactions():
    for transaction in TapTransaction.objects.filter(
        Q(result__exact="") | Q(result__exact="INITIATED")
    ):
        transaction.update_transaction_status()

    return "Success"
