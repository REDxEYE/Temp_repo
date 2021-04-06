from rest_framework import serializers


class CartItemDeleteValidator(serializers.Serializer):
    item_id = serializers.UUIDField()
    quantity = serializers.IntegerField(default=1)


class CartItemPutValidator(serializers.Serializer):
    item_id = serializers.UUIDField()

class ItemGetValidator(serializers.Serializer):
    item_id = serializers.UUIDField()
