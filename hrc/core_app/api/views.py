from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from core_app.api.serializers import CategorySerializer, ProductSerializer
from core_app.models import Category, Product


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CategoriesAPIListView(viewsets.ModelViewSet):
    queryset = Category.objects.select_related().all()
    serializer_class = CategorySerializer


class ProductsAPIListView(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.select_related().all()
    serializer_class = ProductSerializer
