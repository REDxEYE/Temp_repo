from django.urls import path

from online_shop.api_views import *

urlpatterns = [
    path("items/", ItemsApi.as_view(), name="items_api"),
    path("item/", ItemApi.as_view(), name="item_api"),
    path("cart/", ShopingCartApi.as_view(), name="cart_api"),
    path("auth/", AuthApi.as_view(), name="auth_api"),
]
