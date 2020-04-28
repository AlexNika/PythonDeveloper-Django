from django.urls import path
from user_app import views
from django.contrib.auth.views import LogoutView

app_name = 'user_app'
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', views.UserCreateView.as_view(), name='registration'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('user_detail/<slug:slug>/', views.UserDetailView.as_view(), name='user_detail'),
]
