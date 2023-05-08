from django.db.models import Prefetch, Count
from django.db.models import Q
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from product.filter import ProductAttributeFilter
from product.models import Comment, Image, User, Attribute, ProductAttribute, AttributeValue, Brand
from product.pagination import StandardResultsSetPagination
from product.serializers import ProductSerializers, UserSerializers, CommentSerializers, Product, ImageSerializer, \
    AttributeSerializer, ProductAttributeSerializer, ProductAttributeAdvancedFilterSerializer, BrandSerializer


# Create your views here.


class ProductListApiView(ListAPIView):
    # queryset = Product.objects.all().prefetch_related('liked') \
    #     .prefetch_related(
    #     Prefetch('images', queryset=Image.objects.all().select_related('product'))).annotate(
    #     comment_count=Coalesce(Count('comments'), 0, output_field=IntegerField())).annotate(
    #     avg_rating=Coalesce(Round(Avg('comments__rating', default=0)), 0, output_field=IntegerField()))

    serializer_class = ProductSerializers
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        queryset = queryset.prefetch_related('liked')
        queryset = queryset.prefetch_related(
            Prefetch('images', queryset=Image.objects.all().select_related('product')))
        # queryset = queryset.annotate(
        #     comment_count=Coalesce(Count('comments'), 0, output_field=IntegerField()))
        # queryset = queryset.annotate(
        #     avg_rating=Coalesce(Round(Avg('comments__rating', default=0)), 0, output_field=IntegerField()))

        return queryset


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


class ProductAttributeViewSet(ListAPIView):
    queryset = ProductAttribute.objects.all().select_related('product')
    serializer_class = ProductAttributeSerializer
    filter_backends = [ProductAttributeFilter]

    # search_fields = ("attribute_value__value","attribute__id")
    def list(self, request, *args, **kwargs):
        my_filter = ProductAttributeFilter()

        my_filter.parse_character_values(request)

        queryset = self.filter_queryset(self.get_queryset())
        filters = [Q(attribute=attr_id, attribute_value=val_id)
                   for attr_id, values in my_filter.character_values_dict.items()
                   for val_id in values]
        # Combine the Q objects with OR clauses
        print(filters)
        if filters:
            query = filters.pop()

            for f in filters:
                query |= f
            queryset = queryset.filter(query)
        # for attribute_id, attribute_values in my_filter.character_values_dict.items():
        #     value_list = [attribute_value for attribute_value in attribute_values]
        #
        #     queryset = queryset.filter(
        #         Q(attribute=attribute_id) &
        #         Q(attribute_value__in=value_list)
        #     )
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class AttributeViewSet(ListAPIView):
    queryset = Attribute.objects.all().annotate()
    serializer_class = AttributeSerializer



