from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from .forms import SelectionForm, SalesStatsForm
from .calculation import goods_selection, sales_stats


@staff_member_required
def get_selection(request):  # получить выгрузку всех позиций заказа
    selection_modified = None
    form = SelectionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        start_order = form.cleaned_data['start_order']
        end_order = form.cleaned_data['end_order']
        selection_modified, returned_goods_modified = goods_selection(
            start_order, end_order
        )
        return render(
            request, 'stats/selection.html',
            {
                'selection_modified': selection_modified,
                'form': form,
                'returned_goods': returned_goods_modified
            }
        )
    return render(
        request, 'stats/selection.html',
        {
            'selection_modified': selection_modified,
            'form': form
        }
    )


@staff_member_required
def get_sales_stats(request):  # вывод операционных показателей
    form = SalesStatsForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        users_orders_sum = sales_stats(start_date, end_date)
        return render(
            request, 'stats/sales_stats.html',
            {
                'form': form,
                'users_orders_sum': users_orders_sum
            }
        )
    return render(request, 'stats/sales_stats.html', {'form': form})
