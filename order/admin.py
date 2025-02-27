from django.contrib import admin
from .models import Order, OrderItem, Transaction

admin.site.register([Order, OrderItem, Transaction])