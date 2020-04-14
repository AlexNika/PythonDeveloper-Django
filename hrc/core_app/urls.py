from django.urls import path
from core_app import views

app_name = 'core_app'
urlpatterns = [
    # path('', views.main_view, name='main'),
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product_filter/', views.FilterProductsView.as_view(), name='product_filter'),
    path('product_search/', views.SearchProductsView.as_view(), name='product_search'),
    path('product_create/', views.ProductCreateView.as_view(), name='product_create'),
    # path('product_detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product_detail/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product_update/<slug:slug>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('category_create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category_detail/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category_update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    # path('contacts/', views.contacts, name='contacts'),
]
