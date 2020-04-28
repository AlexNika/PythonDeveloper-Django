from django.urls import path
from core_app import views

app_name = 'core_app'
urlpatterns = [
    # path('product_filter/', views.FilterProductsView.as_view(), name='product_filter'),
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product_search/', views.SearchFilterProductsView.as_view(), name='product_search'),
    path('product_filling/', views.ProductUrlFieldFill.as_view(), name='product_filling'),
    path('product_create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product_detail/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product_update/<slug:slug>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('category_create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category_detail/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category_update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
]
