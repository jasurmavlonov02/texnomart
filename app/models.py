from django.contrib.auth.models import AbstractUser
from django.core.validators import integer_validator
from django.db import models
from django.db.models import Model, CharField, ImageField, FloatField, IntegerChoices, TextField, ForeignKey, CASCADE, \
    FileField, DateTimeField, BooleanField, ManyToManyField

from app.managers import UserManager


# Create your models here.


class Product(Model):
    name = CharField(max_length=150)
    price = FloatField()
    description = CharField(max_length=255)
    brand = CharField(max_length=100)
    liked = ManyToManyField('User')

    def __str__(self):
        return self.name


class User(AbstractUser):
    full_name = CharField(max_length=255)
    phone_number = CharField(max_length=13, unique=True)

    objects = UserManager()

    def __str__(self):
        return self.full_name


class Comment(Model):
    class RaitingChoices(IntegerChoices):
        bir = 1
        ikki = 2
        uch = 3
        tort = 4
        besh = 5

    positive_message = CharField(max_length=255)
    negative_message = CharField(max_length=255)
    message = CharField(max_length=255)
    file = FileField(upload_to='file/')
    person = ForeignKey('User', CASCADE, null=True)
    raiting = CharField(max_length=50, choices=RaitingChoices.choices, default=None)

    def __str__(self):
        return self.pk


class ImageModel(Model):
    product = ForeignKey('Product', on_delete=CASCADE, related_name="images")
    image = ImageField(upload_to='img/')


class WishModel(Model):
    user = ForeignKey('User', on_delete=CASCADE, related_name='wishes', null=True)
    product = ForeignKey('Product', on_delete=CASCADE, null=True)
