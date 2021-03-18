from django.urls import path

from online_shop.views import home, listing, item_view, add_item,remove_item

urlpatterns = [
    path("home/", home, name="home"),
    path("listing/", listing, name="listing"),
    path("add_item/<int:item_id>", add_item, name="add_item"),
    path("remove_item/<int:item_id>", remove_item, name="remove_item"),
    path("item_view/<int:item_id>", item_view, name="item_view"),
]
