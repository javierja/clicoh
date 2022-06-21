from django.contrib import admin
from products.models import Product, Order, OrderDetail

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
