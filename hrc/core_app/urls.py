from django.urls import path
from django.views.decorators.cache import cache_page
from core_app import views

app_name = 'core_app'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product_search/', views.SearchFilterProductsView.as_view(), name='product_search'),
    path('product_url_filling/', views.ProductUrlFieldFill.as_view(), name='product_url_filling'),
    path('product_create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product_detail/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product_update/<slug:slug>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('caterory_url_filling/', views.CategoryUrlFieldFill.as_view(), name='category_url_filling'),
    path('category_create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category_detail/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category_update/<slug:slug>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<slug:slug>/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('feedback/', cache_page(600)(views.FeedbackView.as_view()), name='feedback'),
]
