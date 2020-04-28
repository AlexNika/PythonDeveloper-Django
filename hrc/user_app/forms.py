from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CoreUser


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = CoreUser
        fields = ('username', 'password1', 'password2', 'email')

    def save(self, commit=True):
        new_user = CoreUser.objects.create_user(username=self.cleaned_data['username'],
                                                password=self.cleaned_data['password1'],
                                                email=self.cleaned_data['email'])
        new_user.is_active = False
        new_user.save()
        return new_user


class UserForm(forms.ModelForm):

    class Meta:
        model = CoreUser
        # fields = '__all__'
        exclude = ['is_superuser', 'is_staff', 'user_permissions']
