from django.urls import path
from rest_framework.routers import DefaultRouter

from book.views import BookDocumentView
from search.views import ProductDocumentSearch, ProductDocumentViewSet, BrandFacetsView

urlpatterns = [
    path('books/', BookDocumentView.as_view({'get': 'list'}), name='book_view')

]
