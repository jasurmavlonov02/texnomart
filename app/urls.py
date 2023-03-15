from django.urls import path, include
from rest_framework.routers import DefaultRouter
#
# from app.views import CommentListApiView, PersonListApiView, ProductModelViewSet, ProfileModelViewSet, \
#     CommentModelViewSet, ProductDeleteApiView, ImageModelViewSet
from app.views import ProductListApiView, WishListApiView, UserListApiView, ListUsers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# #
# router = DefaultRouter()
# router.register('product', ProductModelViewSet, 'product')
# router.register('person', ProfileModelViewSet, 'person')
# router.register('comment', CommentModelViewSet, 'comment')
# router.register('image', ImageModelViewSet, 'image')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('product-list/', ProductListApiView.as_view(), name='product_list'),
    path('profile-list/', UserListApiView.as_view(), name='profile_list'),
    path('wish-list/', WishListApiView.as_view(), name='wish_list'),

    # path('comment-list/', CommentListApiView.as_view(), name='product_add'),
    # path('person-list/', PersonListApiView.as_view(), name='product_update'),
    # path('product-delete/<int:pk>', ProductDeleteApiView.as_view(), name='product_delete'),
    # path('', include(router.urls)),
    path('user-list/', ListUsers.as_view(), name='user_list'),
]
