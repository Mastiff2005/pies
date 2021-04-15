from django.shortcuts import render
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required

from .forms import SelectionForm, SalesStatsForm
from orders.models import Order, OrderItem
from products.models import Product
from users.models import UserProfile


@staff_member_required
def get_selection(request):  # получить выгрузку всех позиций заказа
    selection_modified = None
    if request.method == 'POST':
        form = SelectionForm(request.POST or None)
        if form.is_valid():
            start_order = form.cleaned_data['start_order']
            end_order = form.cleaned_data['end_order']
            # возвраты
            return_goods = OrderItem.objects.filter(
                order__gte=(start_order)).filter(
                    order__lte=(end_order)).filter(
                        price__lt=0).values('product').annotate(
                            sum=Sum('price')).annotate(
                                qua=Sum('quantity')).order_by('sum')
            return_goods_modified = []
            for item in return_goods:
                price = item['sum']
                quantity = item['qua']
                product = Product.objects.get(id=item['product'])
                return_goods_modified.append({'product': product,
                                              'price': price,
                                              'quantity': quantity})
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
                selected_product = Product.objects.get(id=item['product'])
                product_name = selected_product.name
                product_price = selected_product.price * quantity
                product_price_purc = selected_product.price_purc * quantity
                selection_modified.append(
                    {
                        'product': selected_product,
                        'product_name': product_name,
                        'product_price': product_price,
                        'product_price_purc': product_price_purc,
                        'product_manufacturer': selected_product.manufacturer,
                        'price': price,
                        'quantity': quantity
                    }
                )
            return render(
                request, 'orders/order/selection.html',
                {'selection_modified': selection_modified,
                 'form': form,
                 'return_goods': return_goods_modified}
            )
        return render(
            request, 'orders/order/selection.html',
            {'selection_modified': selection_modified,
             'form': form}
        )
    form = SelectionForm()
    return render(
        request, 'orders/order/selection.html',
        {'selection_modified': selection_modified,
         'form': form}
    )


@staff_member_required
def get_sales_stats(request):  # вывод операционных показателей
    if request.method == 'POST':
        form = SalesStatsForm(request.POST or None)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

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
                        'average': average}
                )

            return render(
                request, 'orders/order/sales_stats.html',
                {
                    'form': form,
                    'users_orders_sum': users_orders_sum
                }
            )
        return render(request, 'orders/order/sales_stats.html', {'form': form})
    form = SalesStatsForm()
    return render(request, 'orders/order/sales_stats.html', {'form': form})
