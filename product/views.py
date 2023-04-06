from django.db.models import Prefetch, Count, Avg, IntegerField
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from django.db.models import OuterRef, Subquery
from product.filter import ProductAttributeFilter
from product.models import Comment, Image, User, Attribute, ProductAttribute
from product.pagination import StandardResultsSetPagination
from product.round import Round
from product.serializers import ProductSerializers, UserSerializers, CommentSerializers, Product, ImageSerializer, \
    AttributeSerializer, ProductAttributeSerializer
from django.db.models import Count, Avg, Sum
from django.db.models.functions import Coalesce


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
    filterset_class = ProductAttributeFilter
    search_fields = ("attribute_value__value",)




class AttributeViewSet(ListAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
