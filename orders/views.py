from django.shortcuts import render, get_object_or_404
import io
from django.http import FileResponse, HttpResponse
# from reportlab.pdfgen import canvas
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.db.models import Sum
# import weasyprint

from .models import Order, OrderItem
from products.models import Product
from users.models import UserProfile
from .forms import OrderCreateForm, SelectionForm, SalesStatsForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST or None)
        form.comment = '111'
        if form.is_valid():
            order = form.save(commit=False)
            if not request.user.is_staff:
                order.user = request.user
            order.save()
            cart_list = []
            for item in cart:
                cart_list.append(item)
                product = item['product']
                OrderItem.objects.create(order=order,
                                         item_number=cart_list.index(item) + 1,
                                         product=item['product'],
                                         price=item['price'],
                                         price_purc=product.price_purc,
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            if not request.user.is_staff:
                send_mail(f'Новый заказ №{order.id} от {request.user}!',
                          'Новый заказ на сайте CAKE POINT. '
                          'Перейдите в панель управления '
                          'для уточнения информации.',
                          'info@cake-point.ru', [
                              'info@cake-point.ru', 'pavel402@bk.ru'
                          ],
                          fail_silently=False)
                send_mail(f'Ваш заказ №{order.id} на CAKE-POINT.ru',
                          'Благодарим за Ваш заказ! С Вами свяжется '
                          'менеджер для уточнения деталей заказа.',
                          'info@cake-point.ru', [f'{request.user.email}'])
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


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    user = order.user
    invoice_num = order.invoice_num
    html = render_to_string('admin/orders/order/pdf.html',
                            {'order': order, 'user': user})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Nakladnaya_{}.pdf"'.format(
        invoice_num
    )
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')]
    )
    return response


@staff_member_required
def get_selection(request):  # получить выгрузку всех позиций заказа
    selection_modified = None
    if request.method == 'POST':
        form = SelectionForm(request.POST or None)
        if form.is_valid():
            start_order = form.cleaned_data['start_order']
            end_order = form.cleaned_data['end_order']

            # начало модификации
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
            # конец модификации

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
                    {'product': selected_product,
                     'product_name': product_name,
                     'product_price': product_price,
                     'product_price_purc': product_price_purc,
                     'product_manufacturer': selected_product.manufacturer,
                     'price': price,
                     'quantity': quantity}
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
def get_sales_stats(request):
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
                    {'user': user,
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


def get_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
