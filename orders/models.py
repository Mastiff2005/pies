from django.db import models
import datetime

from products.models import Product
from users.models import UserProfile


class Order(models.Model):
    invoice_num = models.IntegerField(blank=True, null=True, default=0)
    user = models.ForeignKey(
        UserProfile, on_delete=models.PROTECT,
        blank=True, null=True, related_name='orders'
    )
    comment = models.TextField(max_length=250, blank=True, null=True)
    created = models.DateField(auto_now_add=False, default=datetime.date.today)
    updated = models.DateTimeField(auto_now=True)
    paid_oncard = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_purc_cost(self):
        return sum(item.get_purc_cost() for item in self.items.all())

    def get_returns_cost(self):
        return sum(item.get_cost() for item in self.items.filter(price__lt=0))


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items'
    )
    item_number = models.IntegerField(default=1)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='order_items'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_purc = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    option = models.CharField(max_length=50, blank=True, default='')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_purc_cost(self):
        return self.price_purc * self.quantity
