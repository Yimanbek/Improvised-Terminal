from django.db import models
from product.models import Product
from django.utils import timezone

class Order(models.Model):
    class OrderStatusChoice(models.TextChoices):
        PENDING = 'pending'
        PAID = 'paid'
        CANCELED = 'canceled'
    status = models.CharField(max_length=10, choices=OrderStatusChoice.choices, default=OrderStatusChoice.PENDING)
    total_amount_to_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    odd_money = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.paid_amount}, status: {self.status}'

    def canceled_process(self):
        if self.status != self.OrderStatusChoice.PENDING:
            raise ValueError("The request has already been processed")
        self.status = self.OrderStatusChoice.CANCELED
        self.processed_date = timezone.now()
        self.save()
        return f'Status {self.status}, processed_time {self.processed_date}'

    def paid_process(self, amount):
        if self.status != self.OrderStatusChoice.PENDING:
            raise ValueError("The request has already been processed")
        if self.total_amount_to_paid <= amount:
            self.odd_money = amount - self.total_amount_to_paid
        else:
            self.odd_money = 0

        self.status = self.OrderStatusChoice.PAID
        self.processed_date = timezone.now()
        self.save()
        return self
    
    def remove_amount_from_order(self, amount):
        self.total_amount_to_paid -= amount
        self.save()
    
    def add_amount_to_order(self, total_price):
        self.total_amount_to_paid +=total_price
        self.save()

    def create_transaction(self):
        return Transaction.objects.create(order=self, amount=self.paid_amount)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)

    def __str__(self):
        return f'{self.product.name}, qty: {self.quantity}, total-price: {self.total_price}'

    def save(self, *args, **kwargs):
        self.price = self.product.price
        self.total_price = self.quantity * self.price

        order = self.order
        order.add_amount_to_order(self.total_price)
        product = self.product
        product.get_product(self.quantity)
        super().save(*args, **kwargs)


class Transaction(models.Model):
    order = models.OneToOneField(Order, related_name='order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.amount},  status: {self.order.status}'