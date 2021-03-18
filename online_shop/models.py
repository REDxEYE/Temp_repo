import uuid

import django.contrib.auth
from django.db import models


# Create your models here.

class ShoppingCart(models.Model):
    user = models.ForeignKey(django.contrib.auth.get_user_model(), on_delete=models.CASCADE, related_name='cart')


class ShoppingCartItem(models.Model):
    cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey('Item', on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tags = models.ManyToManyField('Tag')
    name = models.CharField(max_length=256)
    desc = models.TextField()
    shot_desc = models.CharField(max_length=150, default="...")
    image = models.ImageField(upload_to='item_images')
    price = models.IntegerField()

    def __str__(self):
        return f'{self.name}-{self.price}$'


class Tag(models.Model):
    name = models.CharField(max_length=32, default='No tag')
    key = models.CharField(max_length=32, default='no-tag')

    def __str__(self):
        return f'{self.name}-{self.key}'


class Review(models.Model):
    class ReviewScore(models.IntegerChoices):
        STAR_0 = 0
        STAR_1 = 1
        STAR_2 = 2
        STAR_3 = 3
        STAR_4 = 4
        STAR_5 = 5

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    rating = models.IntegerField(choices=ReviewScore.choices)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    user = models.ForeignKey(django.contrib.auth.get_user_model(), on_delete=models.CASCADE)
