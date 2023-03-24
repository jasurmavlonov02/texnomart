from rest_framework.fields import CharField
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, SerializerMethodField, IntegerField

from product.models import Product, Comment, Image, User


class DynamicModelSerializer(ModelSerializer):
    def get_field_names(self, declared_fields, info):
        field_names = super(DynamicModelSerializer, self).get_field_names(declared_fields, info)
        if self.dynamic_fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(self.dynamic_fields)
            excluded_field_names = set(field_names) - allowed
            field_names = tuple(x for x in field_names if x not in excluded_field_names)
        return field_names

    def __init__(self, *args, **kwargs):
        # Don't pass the `fields` or `read_only_fields` arg up to the superclass
        self.dynamic_fields = kwargs.pop('fields', None)
        self.read_only_fields = kwargs.pop('read_only_fields', [])

        # Instantiate the superclass normally
        super(DynamicModelSerializer, self).__init__(*args, **kwargs)


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

    # def get_photo_url(self, obj):
    #     request = self.context.get('request')
    #     photo_url = obj.fingerprint.url
    #     return request.build_absolute_uri(photo_url)


class ProductSerializers(DynamicModelSerializer):
    comment_count = IntegerField()
    avg_rating = IntegerField()

    # images = ImageSerializer(many=True, read_only=True)
    # #
    # uploaded_images = ListField(
    #     child=ImageField(allow_empty_file=False, use_url=False),
    #     write_only=True
    # )

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'price', 'description', 'brand', 'is_liked', 'latest_image', 'comment_count',
            'avg_rating')

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

    # def get_rating_count(self, obj):
    #     rating_count = Comment.objects.filter(product=obj)
    #     return rating_count

# return latest_image_serializer.data.get('image')
# return 'http://127.0.0.1:8000'+latest_image_serializer.data.get('image')


# class WishSerializer(ModelSerializer):
#     class Meta:
#         model = WishModel
#         exclude = ()
