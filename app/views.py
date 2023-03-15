import requests
from django.http import HttpResponse
from django.shortcuts import render
from requests import Response
from rest_framework import status, authentication, permissions
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from app.models import Product, Comment, ImageModel, WishModel, User
from app.serializers import ProductSerializers, UserSerializers, CommentSerializers, Product, ImageSerializer, \
    WishSerializer


# Create your views here.

class ProductListApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
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
# class ImageModelViewSet(ModelViewSet):
#     queryset = ImageModel.objects.all()
#     serializer_class = ImageSerializer
#     lookup_url_kwarg = 'pk'


class WishListApiView(RetrieveAPIView):
    # permission_classes = [IsAuthenticated, ]
    queryset = WishModel.objects.all()
    serializer_class = WishSerializer


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]

    # permission_classes = [permissions.IsAdminUser]

    

