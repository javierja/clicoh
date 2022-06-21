from django.db import models


class Product(models.Model):
    id = models.CharField("product_id", primary_key=True, max_length=150, unique=True)
    name = models.CharField("product_name", max_length=150)
    price = models.FloatField("product_price")
    stock = models.IntegerField("product_stock", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField("date", auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderDetail(models.Model):
    order = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name="order_detail_order", blank=True
    )
    cuantity = models.IntegerField("cuantity", default=0)
    product = models.ManyToManyField("product", related_name="order_product")

    class Meta:
        verbose_name = "Order Detail"
        verbose_name_plural = "Orders Detail"