from django.db import models
from django.forms import ModelForm


class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.IntegerField(default=1)
    manufacturer = models.CharField(max_length=25, default="производитель не выбран")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_purc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shelf_life = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', default='pies\products\static\botw.jpg')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
       return self.name
