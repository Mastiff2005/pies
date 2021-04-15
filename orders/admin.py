from django.contrib import admin
import csv
import datetime
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product', )


def order_detail(obj):
    return mark_safe('<a href="{}">Просмотр</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])))


order_detail.allow_tags = True


def order_cost(obj):
    order = Order.objects.get(id=obj.id)
    return mark_safe(order.get_total_cost())


order_cost.allow_tags = True


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        'attachment; filename={}.csv'.format(opts.verbose_name)
    )
    writer = csv.writer(response)
    fields = [
        field for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice_num', 'user', 'comment', 'paid_oncard',
                    'created', order_cost, order_detail)
    list_filter = ('paid_oncard', 'created')
    inlines = [OrderItemInline]
    actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)
