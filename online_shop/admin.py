from django.contrib import admin

from online_shop.models import Item, Review, ShoppingCart, ShoppingCartItem, Tag, Attribute, AttributeValue


# Register your models here.


class AdminItem(admin.ModelAdmin):
    filter_horizontal = ('attributes',)


class AdminReview(admin.ModelAdmin):
    pass


class AdminTag(admin.ModelAdmin):
    pass


class AdminAttribute(admin.ModelAdmin):
    pass

class AdminAttributeValue(admin.ModelAdmin):
    pass


class AdminShoppingCartItemInline(admin.TabularInline):
    model = ShoppingCartItem
    pass


class AdminShoppingCart(admin.ModelAdmin):
    inlines = [
        AdminShoppingCartItemInline,
    ]
    pass


admin.site.register(Review, AdminReview)
admin.site.register(Tag, AdminTag)
admin.site.register(Attribute, AdminAttribute)
admin.site.register(AttributeValue, AdminAttributeValue)
admin.site.register(Item, AdminItem)
admin.site.register(ShoppingCart, AdminShoppingCart)
