from django.contrib import admin

from product.models import Comment, Product, User, Image, Brand

# Register your models here.

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Brand)
