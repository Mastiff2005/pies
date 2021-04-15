from django.urls import path

from . import views

urlpatterns = [
    path('selection/', views.get_selection, name='get_selection'),
    path('sales-stats/', views.get_sales_stats, name='get_sales_stats'),
]
