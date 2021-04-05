from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "category", "manufacturer", "description", 
                    "shelf_life", "price", "price_purc", "hidden", "image")
    search_fields = ("name",)
    list_filter = ("category", "manufacturer", "hidden")
    empty_value_display = "-пусто-"


admin.site.register(Product, ProductAdmin)
