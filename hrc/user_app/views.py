from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from .forms import UserRegistrationForm, UserForm
from .models import CoreUser


class UserLoginView(LoginView):
    template_name = 'user_app/login.html'


class UserCreateView(LoginRequiredMixin, CreateView):
    model = CoreUser
    template_name = 'user_app/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user_app:login')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CoreUser
    context_object_name = 'user'
    slug_field = 'id'
    template_name = 'user_app/user_detail.html'


class UserListView(LoginRequiredMixin, ListView):
    model = CoreUser
    paginate_by = 10
    context_object_name = 'users'
    form = UserForm
    template_name = 'user_app/user_list.html'
