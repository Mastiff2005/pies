from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('catalogue/pies', views.catalogue_pies, name='catalogue_pies'),
    path('catalogue/cookie', views.catalogue_cookie, name='catalogue_cookie'),
    path(
        'catalogue/super-pies', views.catalogue_superpies,
        name='catalogue_superpies'
    ),
]
