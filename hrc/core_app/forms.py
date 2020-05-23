from django import forms
from django.conf import settings
from django.core.mail import send_mail

from .models import Category, Product


class FeedbackForm(forms.Form):
    name = forms.CharField(required=True, label='Ваше имя')
    email = forms.EmailField(required=True, label='E-mail адрес')
    message = forms.CharField(required=True, widget=forms.Textarea, label='Ваше сообщение')
    firstname = forms.CharField(required=False)
    lastname = forms.CharField(required=False)

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        firstname = self.cleaned_data['firstname']
        lastname = self.cleaned_data['lastname']
        if firstname or lastname:
            print('*** Spam send detected!!! ')
            pass
        else:
            subject = f'Сообщение с портара Hansa Content Library от {name}'
            send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email],
                      fail_silently=True)


class CategoryForm(forms.ModelForm):
    category_short_name = forms.CharField(label='Короткое имя категории',
                                          widget=forms.TextInput(attrs={'placeholder': 'Например: CBI',
                                                                        'class': 'form-control'}))
    category_name = forms.CharField(label='Имя категории',
                                    widget=forms.TextInput(attrs={'placeholder': 'Имя',
                                                                  'class': 'form-control'}))
    category_description = forms.CharField(label='Описание категории',
                                           widget=forms.TextInput(attrs={'placeholder': 'Описание',
                                                                         'class': 'form-control',
                                                                         'required': False}))

    class Meta:
        model = Category
        exclude = ['user']


class ProductForm(forms.ModelForm):
    product_index = forms.CharField(label='Индекс модели',
                                    widget=forms.TextInput(attrs={'placeholder': 'Например: 54290',
                                                                  'class': 'form-control'}))
    product_code = forms.CharField(label='Код модели',
                                   widget=forms.TextInput(attrs={'placeholder': 'Например: FCMW53000',
                                                                 'class': 'form-control'}))
    product_eancode = forms.CharField(label='EAN код модели',
                                      widget=forms.TextInput(attrs={'placeholder': 'Например: 5906006542900',
                                                                    'class': 'form-control'}))

    class Meta:
        model = Product
        exclude = ['user']


class ProductSiteUrl(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product_code', 'product_site_url']


class CategorySiteUrl(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category_short_name', 'category_name', 'category_site_url']