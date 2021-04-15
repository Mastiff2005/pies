from django.shortcuts import get_object_or_404
from django.db.models import Sum

from orders.models import Order, OrderItem
from products.models import Product
from users.models import UserProfile


def goods_selection(start_order, end_order):
    # заказанные товары
    selection = OrderItem.objects.filter(
        order__gte=(start_order)).filter(
            order__lte=(end_order)).filter(
                price__gte=0).values('product').annotate(
                    sum=Sum('price')).annotate(
                        qua=Sum('quantity')).order_by('product')
    selection_modified = []
    for item in selection:
        price = item['sum']
        quantity = item['qua']
        selected_product = get_object_or_404(
            Product, id=item['product']
        )
        product_price = selected_product.price * quantity
        product_price_purc = selected_product.price_purc * quantity
        selection_modified.append(
            {
                'product': selected_product,
                'product_price': product_price,
                'product_price_purc': product_price_purc,
                'price': price,
                'quantity': quantity
            }
        )
    # возвраты
    returned_goods = OrderItem.objects.filter(
        order__gte=(start_order)).filter(
            order__lte=(end_order)).filter(
                price__lt=0).values('product').annotate(
                    sum=Sum('price')).annotate(
                        qua=Sum('quantity')).order_by('sum')
    returned_goods_modified = []
    for item in returned_goods:
        price = item['sum']
        quantity = item['qua']
        returned_product = get_object_or_404(Product, id=item['product'])
        returned_goods_modified.append(
            {
                'product': returned_product,
                'price': price,
                'quantity': quantity
            }
        )
    return selection_modified, returned_goods_modified


def sales_stats(start_date, end_date):
    users = UserProfile.objects.all()
    users_orders_sum = []
    for user in users:
        user_orders = Order.objects.filter(
            created__gte=(start_date)).filter(
                created__lte=(end_date)).filter(
                    user=user
                )
        user_orders_count = user_orders.count()
        user_orders_sum = 0
        user_orders_purc = 0
        user_orders_returns_sum = 0
        for order in user_orders:
            user_orders_sum += order.get_total_cost()
            user_orders_purc += order.get_purc_cost()
            user_orders_returns_sum += order.get_returns_cost()

        # Расчёт операционных показателей
        user_orders_purc = round(user_orders_purc, 0)
        user_orders_returns_sum = abs(
            round(user_orders_returns_sum, 0)
        )
        user_orders_sum = round(
            (user_orders_sum + user_orders_returns_sum), 0
        )
        user_margin = round(
            (user_orders_sum -
                user_orders_purc -
                user_orders_returns_sum), 0
        )
        if user_orders_sum != 0:
            user_margin_percent = round(
                (user_margin / user_orders_sum * 100), 0
            )
        else:
            user_margin_percent = 0
        if user_orders_count != 0:
            average = round((user_orders_sum / user_orders_count), 0)
            user_margin_order = round(
                (user_margin / user_orders_count), 0
            )
        else:
            average = 0
            user_margin_order = 0
        users_orders_sum.append(
            {
                'user': user,
                'user_orders_count': user_orders_count,
                'user_orders_sum': user_orders_sum,
                'user_orders_returns_sum': user_orders_returns_sum,
                'user_orders_purc': user_orders_purc,
                'user_margin': user_margin,
                'user_margin_percent': user_margin_percent,
                'user_margin_order': user_margin_order,
                'average': average
            }
        )
    return users_orders_sum
