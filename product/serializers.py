from django.db.models import Count
from django.db.models.functions import Coalesce
from rest_framework.fields import CharField, ReadOnlyField
from rest_framework.serializers import ModelSerializer, SerializerMethodField, IntegerField

from product.models import Product, Comment, Image, User, Brand, Attribute, AttributeValue, ProductAttribute


class UserSerializers(ModelSerializer):
    username = CharField(max_length=100)

    class Meta:
        model = User
        fields = ('full_name', 'phone_number', 'username')


class CommentSerializers(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ()


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'product', 'image')




class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'title',)


class ProductSerializers(ModelSerializer):
    # images = ImageSerializer(many=True, read_only=True)
    # #
    # uploaded_images = ListField(
    #     child=ImageField(allow_empty_file=False, use_url=False),
    #     write_only=True
    # )

    brand = BrandSerializer(many=False, read_only=False)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'price', 'description', 'brand', 'is_liked', 'latest_image', 'comment_count',
            'avg_rating', 'main_characters'
        )

    # def create(self, validated_data):
    #     uploaded_images = validated_data.pop("uploaded_images")
    #     product = Product.objects.create(**validated_data)
    #
    #     for image in uploaded_images:
    #         new_product_image = ImageModel.objects.create(product=product, image=image)
    #
    #     return product

    latest_image = SerializerMethodField()
    is_liked = SerializerMethodField()
    comment_count = SerializerMethodField()
    avg_rating = SerializerMethodField()
    main_characters = SerializerMethodField()

    def get_main_characters(self, obj):
        characters = ProductAttribute.objects.filter(product=obj).values_list(
            'attribute__title',
            'attribute_value__value',
        )
        character_data = [
            {'name': name, 'value': value, }
            for
            name, value, in
            characters]
        return character_data

    #
    def get_latest_image(self, obj):

        latest_image = obj.images.all()

        if len(latest_image) == 0 or not latest_image:
            return None

        latest_image = latest_image[0]
        latest_image_serializer = ImageSerializer(latest_image)

        request = self.context.get('request')
        photo_url = latest_image.image.url
        return request.build_absolute_uri(photo_url)

    def get_is_liked(self, instance):
        user = self.context.get('request').user

        liked = instance.liked.all()

        if user in liked:
            return True
        return False

    def get_comment_count(self, obj):
        counts = Comment.objects.filter(product=obj).count()
        return counts

    def get_avg_rating(self, obj):
        comments = obj.comments.all()
        if comments:
            total_rating = sum(comment.rating for comment in comments)
            return round(total_rating / len(comments))
        else:
            return 0


# return latest_image_serializer.data.get('image')
# return 'http://127.0.0.1:8000'+latest_image_serializer.data.get('image')


class ProductAttributeSerializer(ModelSerializer):
    product = ProductSerializers(many=False, read_only=True)

    class Meta:
        model = ProductAttribute
        fields = ('attribute', 'attribute_value', 'product')


class AttributeValueSerializer(ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ('id', 'value')


class AttributeSerializer(ModelSerializer):
    values = SerializerMethodField()

    def get_values(self, obj):
        # values = obj.productattribute_set.select_related('attribute_value').values_list('attribute_value__id',
        #                                                                                 'attribute_value__value')
        values = ProductAttribute.objects.filter(attribute=obj).annotate(
            count=Coalesce(Count('product'), 0)).values_list('attribute_value__id',
                                                             'attribute_value__value', 'count',
                                                             )

        # serialized_values = ProductAttributeSerializer(values, many=True)
        attr_data = [
            {'attr_value_id': id, 'attr_value': value, 'attribute_title': obj.title, 'count': count}
            for
            id, value, count in
            values]
        return attr_data

    class Meta:
        model = Attribute
        fields = ('id', 'title', 'values')


class ProductAttributeAdvancedFilterSerializer(ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ('attribute', 'attribute_value', 'product',)
