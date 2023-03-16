from itertools import count

import requests
from django.db.models import Prefetch, Count
from django.http import HttpResponse
from django.shortcuts import render
from requests import Response
from rest_framework import status, authentication, permissions
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from product import models
from product.models import Product, Comment, Image, User
from product.pagination import StandardResultsSetPagination

from product.serializers import ProductSerializers, UserSerializers, CommentSerializers, Product, ImageSerializer


# Create your views here.


class ProductListApiView(ListAPIView):
    queryset = Product.objects.all().prefetch_related('liked') \
                   .prefetch_related(
        Prefetch('images', queryset=Image.objects.all().select_related('product'))).annotate(
        comment_count=Count('comments'))

    # queryset = Product.objects.all()[:50]
    serializer_class = ProductSerializers
    pagination_class = StandardResultsSetPagination

    # def get_queryset(self):
    #     return Product.objects.all().prefetch_related('liked')[:12]

    # permission_classes = [IsAuthenticated, ]


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    # permission_classes = [IsAuthenticated, ]


class CommentListApiView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers


# #
# # class ProductAddApiView(CreateAPIView):
# #     queryset = Product.objects.all()
# #     serializer_class = ProductSerializers
# #
# #
# # class ProductUpadateApiView(UpdateAPIView):
# #     queryset = Product.objects.all()
# #     serializer_class = ProductSerializers
# #     lookup_url_kwarg = 'pk'
# #
# #
# # class ProductDeleteApiView(DestroyAPIView):
# #     queryset = Product.objects.all()
# #     serializer_class = ProductSerializers
# #     lookup_url_kwarg = 'pk'
# #
# #
# # class ProductModelViewSet(ModelViewSet):
# #     queryset = Product.objects.all()
# #     serializer_class = ProductSerializers
# #     lookup_url_kwarg = 'pk'
#
#
# class ProfileModelViewSet(ModelViewSet):
#     queryset = Person.objects.all()
#     serializer_class = PersonSerializers
#     lookup_url_kwarg = 'pk'

#
# class CommentModelViewSet(ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializers
#     lookup_url_kwarg = 'pk'
#
#
class ImageModelViewSet(ModelViewSet):
    # queryset = Image.objects.all()
    serializer_class = ImageSerializer
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        return Image.objects.all().select_related('product_id')
