from django.contrib import admin
from django.urls import include, path  # , re_path  # добавлен re_path
from django.conf.urls import handler404, handler500  # , url новый импорт
from django.conf.urls.static import static
from django.conf import settings
# новые импорты
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.views.static import serve

handler404 = 'homepage.views.page_not_found'  # noqa
handler500 = 'homepage.views.server_error'  # noqa


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'), name='api'),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('', include('homepage.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('stats/', include('stats.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    # urlpatterns += (path('__debug__', include(debug_toolbar.urls)),)  # изм.

# urlpatterns += staticfiles_urlpatterns()  # изм.
# urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),]  # изм.
# urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT,}),]  # изм.
