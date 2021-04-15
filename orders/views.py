from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail

from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST or None)
        if form.is_valid():
            order = form.save(commit=False)
            if not request.user.is_staff:
                order.user = request.user
            order.save()
            cart_list = []
            for item in cart:
                cart_list.append(item)
                product = item['product']
                OrderItem.objects.create(
                    order=order,
                    item_number=cart_list.index(item) + 1,
                    product=item['product'],
                    price=item['price'],
                    price_purc=product.price_purc,
                    quantity=item['quantity']
                )
            # очистка корзины
            cart.clear()
            if not request.user.is_staff:
                send_mail(f'Новый заказ №{order.id} от {request.user}!',
                          'Новый заказ на сайте CAKE POINT. '
                          'Перейдите в панель управления '
                          'для уточнения информации.',
                          'info@test.test', [
                              'info@test.test'
                          ],
                          fail_silently=False)
                send_mail(f'Ваш заказ №{order.id} на CAKE-POINT.ru',
                          'Благодарим за Ваш заказ! С Вами свяжется '
                          'менеджер для уточнения деталей заказа.',
                          'info@test.test', [f'{request.user.email}'])
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    user = order.user
    return render(
        request, 'admin/orders/order/detail.html',
        {'order': order, 'user': user}
    )
