from django.contrib import admin
from django.urls import include, path, re_path  # добавлен re_path
from django.conf.urls import url, handler404, handler500  # новый импорт
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # новый импорт
# from django.views.static import serve  # Новый импорт

from homepage import views as home_views
from orders import views as orders_views

handler404 = 'homepage.views.page_not_found'  # noqa
handler500 = 'homepage.views.server_error'  # noqa


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('', home_views.index, name='index'),
    path('contact/', home_views.contact, name='contact'),
    path('catalogue/', home_views.catalogue, name='catalogue'),
    path('catalogue/pies', home_views.catalogue_pies, name='catalogue_pies'),
    path('catalogue/cookie', home_views.catalogue_cookie, name='catalogue_cookie'),
    path('catalogue/super-pies', home_views.catalogue_superpies, name='catalogue_superpies'),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    # url(r'^admin/', admin.site.urls),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('selection/', orders_views.get_selection, name='get_selection'),
    path('sales-stats', orders_views.get_sales_stats, name='get_sales_stats'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += (path('__debug__', include(debug_toolbar.urls)),)  # изм.
    
# urlpatterns += staticfiles_urlpatterns()  # изм.
# urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),]  # изм.
# urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT,}),]  # изм.
   