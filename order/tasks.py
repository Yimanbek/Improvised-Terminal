import logging
from celery import shared_task
from django.utils import timezone
from .models import Order

@shared_task(
    autoretry_for=(Exception,),
    retry_kwargs={
        'max_retries': 5,
        'countdown': 30,
    }
)
def checking_unpaid_orders():
    today = timezone.now().date()
    orders = Order.objects.filter(created_at__date__lt = today, status = Order.OrderStatusChoice.PENDING)

    for order in orders:
        order.canceled_process()
