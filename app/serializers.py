from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ImageField, ListField, \
    PrimaryKeyRelatedField
from django.contrib.sites.shortcuts import get_current_site
from app.models import Product, Comment, ImageModel, WishModel, User


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
        model = ImageModel
        fields = ('id', 'product', 'image')

    # def get_photo_url(self, obj):
    #     request = self.context.get('request')
    #     photo_url = obj.fingerprint.url
    #     return request.build_absolute_uri(photo_url)


class ProductSerializers(ModelSerializer):
    # images = ImageSerializer(many=True, read_only=True)
    # #
    # uploaded_images = ListField(
    #     child=ImageField(allow_empty_file=False, use_url=False),
    #     write_only=True
    # )

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description', 'brand', 'latest_image', 'liked', 'is_liked')

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

    def get_latest_image(self, obj):
        latest_image = ImageModel.objects.filter(product=obj).latest('id')
        latest_image_serializer = ImageSerializer(latest_image)
        request = self.context.get('request')
        photo_url = latest_image.image.url
        return request.build_absolute_uri(photo_url)

    def get_is_liked(self, instance):
        user = self.context.get('request').user

        liked = instance.liked.all()

        print('---------')
        print(liked)
        print('---------')
        if user in liked:
            return True
        return False


# return latest_image_serializer.data.get('image')
# return 'http://127.0.0.1:8000'+latest_image_serializer.data.get('image')


class WishSerializer(ModelSerializer):
    class Meta:
        model = WishModel
        exclude = ()
