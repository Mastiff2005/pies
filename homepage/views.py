from django.shortcuts import render

from products.models import Product
from cart.forms import CartAddProductForm
from cart.cart import Cart


def index(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def catalogue(request):
    keyword = request.GET.get("q", None)
    if keyword:
        products = Product.objects.filter(
            name__icontains=keyword).filter(
                hidden=False).order_by('name')
    else:
        products = Product.objects.filter(
            category=1).filter(hidden=False).order_by('name')
    cart_product_form = CartAddProductForm()
    cart = Cart(request)
    return render(
        request,
        'catalogue.html',
        {
            'products': products,
            'boxes': products,
            'keyword': keyword,
            'cart': cart,
            'cart_product_form': cart_product_form}
    )


def catalogue_pies(request):
    keyword = request.GET.get("q", None)
    if keyword:
        products = Product.objects.filter(
            name__icontains=keyword).filter(
                hidden=False).order_by('name')
    else:
        products = Product.objects.filter(
            category=2).filter(hidden=False).order_by('name')
    cart_product_form = CartAddProductForm()
    cart = Cart(request)
    return render(
        request,
        'catalogue.html',
        {
            'products': products,
            'pies': products,
            'keyword': keyword,
            'cart': cart,
            'cart_product_form': cart_product_form
        }
    )


def catalogue_cookie(request):
    keyword = request.GET.get("q", None)
    if keyword:
        products = Product.objects.filter(
            name__icontains=keyword).filter(
                hidden=False).order_by('name')
    else:
        products = Product.objects.filter(
            category=3).filter(hidden=False).order_by('name')
    cart_product_form = CartAddProductForm()
    cart = Cart(request)
    return render(
        request,
        'catalogue.html',
        {
            'products': products,
            'cookie': products,
            'keyword': keyword,
            'cart': cart,
            'cart_product_form': cart_product_form
        }
    )


def catalogue_superpies(request):
    keyword = request.GET.get("q", None)
    if keyword:
        products = Product.objects.filter(
            name__icontains=keyword).filter(
                hidden=False).order_by('name')
    else:
        products = Product.objects.filter(
            category=4).filter(hidden=False).order_by('name')
    cart_product_form = CartAddProductForm()
    cart = Cart(request)
    return render(
        request,
        'catalogue.html',
        {
            'products': products,
            'super_pies': products,
            'keyword': keyword,
            'cart': cart,
            'cart_product_form': cart_product_form
        }
    )


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
