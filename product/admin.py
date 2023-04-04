from django.contrib import admin

from product.models import Comment, Product, User, Image, Brand, Attribute, AttributeValue, ProductAttribute

# Register your models here.

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Brand)


# admin.site.register(Attribute)


# admin.site.register(AttributeValue)


# admin.site.register(ProductAttribute)

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'attribute', 'attribute_value']


admin.site.register(ProductAttribute, ProductAttributeAdmin)


class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']


admin.site.register(AttributeValue, AttributeValueAdmin)


class AttributeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


admin.site.register(Attribute, AttributeAdmin)
