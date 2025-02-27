from django.db import models

class Product(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name} - price: {self.price}'
    
    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.status = True
        else:
            self.status = False

        super().save(*args,**kwargs)

    def get_product(self, quantity):
        if self.quantity < quantity:
            raise ValueError("Not enough stock")
        self.quantity -= quantity
        self.save()
    
    def rollback_product(self, quantity):
        self.quantity += quantity
        self.save()