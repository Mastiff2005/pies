from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from cart.cart import Cart


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def cart_view(request):
    cart = Cart(request)
    items = []
    for item in cart:
        items.append(
            {
                'name': (item['product']).name,
                'quantity': item['quantity'],
                'price': item['total_price']
            }
        )
    quantity = len(items)
    total_price = cart.get_total_price()
    return Response(
        {'total_price': total_price,
         'quantity': quantity,
         'items': items}
    )
