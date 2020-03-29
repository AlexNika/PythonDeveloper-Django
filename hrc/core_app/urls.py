from django.urls import path
from core_app import views

app_name = 'core_app'
urlpatterns = [
    path('', views.main_view, name='main'),
    path('contacts/', views.contacts, name='contacts'),
    path('create_category/', views.create_category, name='create_category'),
]
