from django.conf.urls import url
from django.urls import path

from . import views


urlpatterns = [
    # url(r'^create/$', views.order_create, name='order_create'),
    path('create/', views.order_create, name='order_create'),
    path('getpdf/', views.get_pdf, name='get_pdf'),
    #path('admin/order/', views.admin_order_detail, name='admin_order_detail'),
    url(r'^admin/order/(?P<order_id>\d+)/$', views.admin_order_detail, name='admin_order_detail'),
    #path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
    url(r'^admin/order/(?P<order_id>\d+)/pdf/$', views.admin_order_pdf, name='admin_order_pdf'),
]
