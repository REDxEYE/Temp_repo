from rest_framework import serializers

from .models import Item, ShoppingCartItem, ShoppingCart, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'key']


class ItemSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    tags = serializers.ListSerializer(child=TagSerializer())
    class Meta:
        model = Item
        fields = ['id', 'tags', 'name', 'desc', 'shot_desc', 'image', 'price']
        depth = 1


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = ShoppingCartItem
        fields = ['item', 'quantity', ]
        depth = 1


class ShoppingCartSerializer(serializers.ModelSerializer):
    items = serializers.ListSerializer(child=ShoppingCartItemSerializer())

    class Meta:
        model = ShoppingCart
        fields = ['items']
        depth = 1
