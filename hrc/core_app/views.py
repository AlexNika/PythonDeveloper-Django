from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F, Q
from django.shortcuts import render, HttpResponseRedirect
from django.template.context_processors import csrf
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import ContextMixin, View

from .forms import ContactForm, CategoryForm, ProductForm, ProductFilter
from .models import Category, Product


# def contacts(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             message = form.cleaned_data['message']
#             subject = f'Сообщение с портара Hansa Content Library от {name}'
#             send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email],
#                       fail_silently=True)
#             return HttpResponseRedirect(reverse('core_app:main'))
#         else:
#             return render(request, 'core_app/contacts.html', context={'form': form})
#     else:
#         form = ContactForm()
#         return render(request, 'core_app/contacts.html', context={'form': form})


class CategoryContextMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class StatusContextMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        statuses = Product.objects.order_by('product_status').distinct().values_list('product_status')
        us = []
        for i in statuses:
            us.extend(list(i))
        context = super().get_context_data(**kwargs)
        context['unique_status'] = us
        return context


class ContactsView(View, CategoryContextMixin, StatusContextMixin):

    class Meta:
        abstract = True

    template_name = 'core_app/contacts.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        # context.update(csrf(request))
        # context['form'] = ContactForm()
        return render(request, template_name=self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = f'Сообщение с портара Hansa Content Library от {name}'
            send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[email], fail_silently=True)
            return HttpResponseRedirect(reverse('core_app:product_list'))
        else:
            return render(request, 'core_app/contacts.html', context={'form': form})


class CategoryListView(ListView, CategoryContextMixin, StatusContextMixin):
    model = Category
    template_name = 'core_app/category_list.html'


class CategoryDetailView(DetailView, CategoryContextMixin, StatusContextMixin):
    model = Category
    template_name = 'core_app/category_detail.html'


class CategoryCreateView(CreateView, CategoryContextMixin, StatusContextMixin):
    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('core_app:category_list')
    template_name = 'core_app/category_create.html'


class CategoryUpdateView(UpdateView, CategoryContextMixin, StatusContextMixin):
    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('core_app:category_list')
    template_name = 'core_app/category_update.html'


class CategoryDeleteView(DeleteView, CategoryContextMixin, StatusContextMixin):
    model = Category
    success_url = reverse_lazy('core_app:category_list')
    template_name = 'core_app/category_delete_confirm.html'


class ProductListView(ListView, CategoryContextMixin, StatusContextMixin):
    model = Product
    paginate_by = 10
    context_object_name = 'products'
    form = ProductForm
    template_name = 'core_app/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


class ProductDetailView(DetailView, CategoryContextMixin, StatusContextMixin):
    model = Product
    context_object_name = 'product'
    slug_field = 'product_index'
    template_name = 'core_app/product_detail.html'


class ProductCreateView(CreateView, CategoryContextMixin, StatusContextMixin):
    form_class = ProductForm
    model = Product
    success_url = reverse_lazy('core_app:product_list')
    template_name = 'core_app/product_create.html'


class ProductUpdateView(UpdateView, CategoryContextMixin, StatusContextMixin):
    form_class = ProductForm
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('core_app:category_list')
    slug_field = 'product_index'
    template_name = 'core_app/product_update.html'


class FilterProductsView(ListView, CategoryContextMixin, StatusContextMixin):
    model = Product
    paginate_by = 10
    context_object_name = 'products'
    form = ProductForm
    template_name = 'core_app/product_filter_result.html'

    # def get(self, request, *args, **kwargs):
    #     product_status = kwargs['product_status']
    #     return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Product.objects.filter(product_status__in=self.request.GET.getlist('product_status'))
        return queryset

    def get_context_data(self, **kwargs):
        unique_status = Product.objects.order_by('product_status').distinct().values_list('product_status')
        us = []
        for i in unique_status:
            us.extend(list(i))
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        context['unique_status'] = us
        return context


class SearchProductsView(ListView, CategoryContextMixin, StatusContextMixin):
    model = Product
    paginate_by = 10
    context_object_name = 'products'
    slug_field = 'product_index'
    template_name = 'core_app/product_search_result.html'

    def get_queryset(self):
        queryset = Product.objects.filter(
            Q(product_index__icontains=self.request.GET.get('q')) |
            Q(product_code__icontains=self.request.GET.get('q')) |
            Q(product_eancode__icontains=self.request.GET.get('q')))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context
