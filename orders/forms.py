import datetime as dt
from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'comment']
        
        
class SelectionForm(forms.Form):
    start_order = forms.IntegerField(required=False, label='Начальный заказ')
    end_order = forms.IntegerField(required=False, label='Конечный заказ')


class SalesStatsForm(forms.Form):
	start_date = forms.DateField(label='Начальная дата', initial='2000-01-01')
	end_date = forms.DateField(label='Конечная дата',
							   initial=dt.datetime.strftime(
							   dt.date.today(), '%Y-%m-%d'))
        