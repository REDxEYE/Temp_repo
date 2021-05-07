from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth import CsrfExemptSessionAuthentication
from .models import ShoppingCart, ShoppingCartItem, Item
from .serializers import ItemSerializer, ShoppingCartItemSerializer, ShoppingCartSerializer
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from .validators import CartItemDeleteValidator, CartItemPutValidator, ItemGetValidator


class AuthApi(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @csrf_exempt
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'success': True})
            else:
                return Response({'success': False, 'reason': 'User inactive'})
        else:
            return Response({'success': False, 'reason': 'Invalid username or password'})


class ItemsApi(APIView):
    def get(self, request):
        items = Item.objects.all()
        serialized_items = ItemSerializer(items, many=True)
        return Response({"items": serialized_items.data})


class ItemApi(APIView):
    def get(self, request):
        serializer = ItemGetValidator(data=request.data)
        if serializer.is_valid():
            item = get_object_or_404(Item, id=request.data['item_id'])
            serialized_items = ItemSerializer(item)
            return Response(serialized_items.data)
        return Response({'success': False, 'reason': 'GET parameters validation failed'})


@method_decorator(login_required, name='dispatch')
class ShopingCartApi(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        user = request.user
        cart, created = ShoppingCart.objects.get_or_create(user=user)
        if created:
            cart.save()
        serialized_items = ShoppingCartSerializer(cart)
        return Response(serialized_items.data)

    @csrf_exempt
    def put(self, request):
        serializer = CartItemPutValidator(data=request.data)
        if serializer.is_valid():
            item = get_object_or_404(Item, pk=request.data['item_id'])
            user = request.user
            cart, created = ShoppingCart.objects.get_or_create(user=user)
            if created:
                cart.save()
            cart_item, created = ShoppingCartItem.objects.get_or_create(cart=cart, item=item)
            if not created:
                cart_item.quantity += 1

            cart_item.save()
            serialized = ShoppingCartItemSerializer(cart_item)
            return Response({'success': True, 'item': serialized.data})
        return Response({'success': False, 'reason': 'PUT parameters validation failed'})

    @csrf_exempt
    def delete(self, request):
        serializer = CartItemDeleteValidator(data=request.data)
        if serializer.is_valid():
            item = get_object_or_404(ShoppingCartItem, item_id=request.data['item_id'])
            quantity = int(request.data.get('quantity', 1))
            quantity = min(quantity, item.quantity)
            if item.quantity == quantity:
                item.delete()
                return Response({'success': True})
            elif item.quantity > quantity:
                item.quantity -= quantity
                item.save()
                return Response({'success': True})
            else:
                return Response({'success': False, 'reason': 'Invalid quantity'})

        return Response({'success': False, 'reason': 'DELETE parameters validation failed'})
