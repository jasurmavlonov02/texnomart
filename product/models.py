from django.contrib.auth.models import AbstractUser
from django.core.validators import integer_validator
from django.db import models
from django.db import models

from product.managers import UserManager


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.FloatField()
    description = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    liked = models.ManyToManyField('User', related_name='liked')

    def __str__(self):
        return self.name


class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13, unique=True)

    objects = UserManager()

    def __str__(self):
        return self.full_name


class Comment(models.Model):
    class RaitingChoices(models.IntegerChoices):
        nol = 0
        bir = 1
        ikki = 2
        uch = 3
        tort = 4
        besh = 5

    positive_message = models.CharField(max_length=255, null=True, blank=True)
    negative_message = models.CharField(max_length=255, null=True, blank=True)
    message = models.CharField(max_length=255)
    file = models.FileField(upload_to='file/', null=True, blank=True)
    user = models.ForeignKey('User', models.CASCADE, null=True)
    product = models.ForeignKey('Product', models.CASCADE, 'comments')
    rating = models.IntegerField(choices=RaitingChoices.choices, default=RaitingChoices.nol)

    def __str__(self):
        return self.message


class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="images", null=True)
    image = models.ImageField(upload_to='img/')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', ]