from django import forms
from .models import Category


class ContactForm(forms.Form):
    name = forms.CharField(required=True, label='Ваше имя')
    email = forms.EmailField(required=True, label='E-mail адрес')
    message = forms.CharField(required=True, widget=forms.Textarea, label='Ваше сообщение')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
