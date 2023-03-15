from django.contrib import admin

from app.models import Comment, Product, ImageModel, WishModel, User

# Register your models here.

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Product)
admin.site.register(ImageModel)
admin.site.register(WishModel)
