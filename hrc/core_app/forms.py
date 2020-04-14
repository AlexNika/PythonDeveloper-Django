from django import forms
from .models import Category, Product


class ContactForm(forms.Form):
    name = forms.CharField(required=True, label='Ваше имя')
    email = forms.EmailField(required=True, label='E-mail адрес')
    message = forms.CharField(required=True, widget=forms.Textarea, label='Ваше сообщение')


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
        fields = '__all__'


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

    # product_category = forms.ModelChoiceField(queryset=Category.objects.filter(category_short_name__exact='CBI'))

    class Meta:
        model = Product
        fields = '__all__'


class ProductFilter(forms.ModelForm):

    product_status = forms.ModelMultipleChoiceField(queryset=Product.objects.all(),
                                                    widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Product
        fields = ('product_status', )
