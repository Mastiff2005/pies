from django.urls import path
# from rest_framework.routers import DefaultRouter

from .views import cart_view

app_name = 'api'

# router = DefaultRouter()

urlpatterns = [
    path('cart_view/', cart_view, name='cart_view'),
    # path('', include(router.urls)),
]
