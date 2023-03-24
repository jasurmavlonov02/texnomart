from django.urls import path, include
from rest_framework.routers import DefaultRouter
#
# from product.views import CommentListApiView, PersonListApiView, ProductModelViewSet, ProfileModelViewSet, \
#     CommentModelViewSet, ProductDeleteApiView, ImageModelViewSet
from product.views import ProductListApiView, UserListApiView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.decorators.cache import cache_page

# #
# router = DefaultRouter()
# router.register('product', ProductModelViewSet, 'product')
# router.register('person', ProfileModelViewSet, 'person')
# router.register('comment', CommentModelViewSet, 'comment')
# router.register('image', ImageModelViewSet, 'image')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('product-list/', cache_page(60)(ProductListApiView.as_view()), name='product_list'),
    path('profile-list/', UserListApiView.as_view(), name='profile_list'),

    # path('comment-list/', CommentListApiView.as_view(), name='product_add'),
    # path('person-list/', PersonListApiView.as_view(), name='product_update'),
    # path('product-delete/<int:pk>', ProductDeleteApiView.as_view(), name='product_delete'),
    # path('', include(router.urls)),
]
