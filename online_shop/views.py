from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from online_shop.models import Item, Review, ShoppingCart, ShoppingCartItem, Tag, Attribute, AttributeValue
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from online_shop.forms import CheckoutForm


# Create your views here.
@login_required(login_url='/accounts/login')
def logout_shortcut(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def home(request):
    items = Item.objects.all().order_by('id')[:5]

    return render(request, 'online_shop/home.html', context={'active': items[0], 'other': items[1:]})


def listing(request):
    item_filter = request.GET.get('filter', None)
    attribute_name = request.GET.get('attribute_name', None)
    attribute_value = request.GET.get('attribute_value', None)
    if item_filter is not None:
        items = Item.objects.filter(tag__key__iexact=item_filter).all()
    elif attribute_value and attribute_value:
        items = Item.objects.filter(attributes__attribute__key__iexact=attribute_name,
                                    attributes__value__icontains=attribute_value).all()
    else:
        items = Item.objects.all()
    tags = Tag.objects.all()

    rows = []
    cur_row = []
    for item in items:
        if len(cur_row) == 3:
            rows.append(cur_row)
            cur_row = [item]
        else:
            cur_row.append(item)
    if cur_row not in rows:
        rows.append(cur_row)
    available_attributes = {}

    for item in items:
        for attr_value in AttributeValue.objects.filter(item=item):
            attr_value: AttributeValue
            available_attributes.setdefault(attr_value.attribute, set()).add(attr_value.value)

    return render(request, 'online_shop/listing.html',
                  context={'item_rows': rows, 'all_tags': tags, 'available_attributes': available_attributes})


@login_required(login_url='/accounts/login')
def add_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    user = request.user
    cart, created = ShoppingCart.objects.get_or_create(user=user)
    if created:
        cart.save()
    cart_item, created = ShoppingCartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity += 1

    cart_item.save()

    return redirect(request.headers['referer'])


@login_required(login_url='/accounts/login')
def remove_item(request, item_id):
    item = get_object_or_404(ShoppingCartItem, pk=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect(request.headers['referer'])


def item_view(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'online_shop/item_view.html', context={'item': item})


@login_required(login_url='/accounts/login')
def checkout(request):
    user = request.user
    sc = ShoppingCartItem.objects.filter(cart__user=user)
    form = CheckoutForm()
    return render(request, 'online_shop/checkout.html', context={'items': sc, 'form': form})
