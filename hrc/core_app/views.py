from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import ContextMixin

from .forms import FeedbackForm, CategoryForm, ProductForm, ProductSiteUrl
from .models import Category, Product


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


class FeedbackView(FormView, CategoryContextMixin, StatusContextMixin):
    template_name = 'core_app/feedback.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('core_app:product_list')

    def form_valid(self, form):
        form.send_email()
        return super(FeedbackView, self).form_valid(form)


class CategoryListView(ListView, CategoryContextMixin, StatusContextMixin):
    model = Category
    template_name = 'core_app/category_list.html'


class CategoryDetailView(DetailView, CategoryContextMixin, StatusContextMixin):
    model = Category
    template_name = 'core_app/category_detail.html'


class CategoryCreateView(LoginRequiredMixin, CreateView, CategoryContextMixin, StatusContextMixin):
    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('core_app:category_list')
    template_name = 'core_app/category_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView, CategoryContextMixin, StatusContextMixin):
    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('core_app:category_list')
    template_name = 'core_app/category_update.html'


class CategoryDeleteView(LoginRequiredMixin, DeleteView, CategoryContextMixin, StatusContextMixin):
    model = Category
    success_url = reverse_lazy('core_app:category_list')
    template_name = 'core_app/category_delete_confirm.html'


class ProductListView(ListView, CategoryContextMixin, StatusContextMixin):
    model = Product
    paginate_by = 10
    context_object_name = 'products'
    form = ProductForm
    template_name = 'core_app/product_list.html'


class ProductDetailView(DetailView, CategoryContextMixin, StatusContextMixin):
    model = Product
    context_object_name = 'product'
    slug_field = 'product_index'
    template_name = 'core_app/product_detail.html'


class ProductCreateView(LoginRequiredMixin, CreateView, CategoryContextMixin, StatusContextMixin):
    form_class = ProductForm
    model = Product
    success_url = reverse_lazy('core_app:product_list')
    template_name = 'core_app/product_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProductCreateView, self).form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView, CategoryContextMixin, StatusContextMixin):
    form_class = ProductForm
    model = Product
    paginate_by = 10
    context_object_name = 'product'
    success_url = reverse_lazy('core_app:product_list')
    slug_field = 'product_index'
    template_name = 'core_app/product_update.html'


class SearchFilterProductsView(ListView, CategoryContextMixin, StatusContextMixin):
    model = Product
    paginate_by = 10
    context_object_name = 'products'
    slug_field = 'product_index'
    template_name = 'core_app/product_search_result.html'

    def get_queryset(self):
        sphrase = self.request.GET.get('sphrase')
        status = self.request.GET.get('status')
        category = self.request.GET.get('category')
        if (sphrase == '') and (status != 'all') and (category == 'all'):
            queryset = Product.objects.filter(product_status__icontains=status)
            return queryset
        elif (sphrase == '') and (status == 'all') and (category != 'all'):
            queryset = Product.objects.filter(product_category=Category.objects.get(category_short_name=category).id)
            return queryset
        elif (sphrase == '') and (status != 'all') and (category != 'all'):
            queryset = Product.objects.filter(
                Q(product_status__icontains=status),
                Q(product_category=Category.objects.get(category_short_name=category).id))
            return queryset
        elif (sphrase != '') and (status == 'all') and (category == 'all'):
            queryset = Product.objects.filter(
                Q(product_index__icontains=sphrase) |
                Q(product_code__icontains=sphrase) |
                Q(product_eancode__icontains=sphrase))
            return queryset
        elif (sphrase != '') and (status != 'all') and (category == 'all'):
            queryset = Product.objects.filter(
                Q(product_index__icontains=sphrase) |
                Q(product_code__icontains=sphrase) |
                Q(product_eancode__icontains=sphrase),
                Q(product_status__icontains=status))
            return queryset
        elif (sphrase != '') and (status == 'all') and (category != 'all'):
            queryset = Product.objects.filter(
                Q(product_index__icontains=sphrase) |
                Q(product_code__icontains=sphrase) |
                Q(product_eancode__icontains=sphrase),
                Q(product_category=Category.objects.get(category_short_name=category).id))
            return queryset
        elif (sphrase != '') and (status != 'all') and (category != 'all'):
            queryset = Product.objects.filter(
                Q(product_index__icontains=sphrase) |
                Q(product_code__icontains=sphrase) |
                Q(product_eancode__icontains=sphrase),
                Q(product_status__icontains=status),
                Q(product_category=Category.objects.get(category_short_name=category).id))
            return queryset
        else:
            queryset = Product.objects.all()
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sphrase'] = self.request.GET.get('sphrase')
        context['status'] = self.request.GET.get('status')
        context['category'] = self.request.GET.get('category')
        return context


class ProductUrlFieldFill(LoginRequiredMixin, ListView):
    form_class = ProductSiteUrl
    model = Product
    context_object_name = 'products'
    success_url = reverse_lazy('core_app:product_list')
    template_name = 'core_app/product_site_url_filling.html'

    def get_queryset(self):
        queryset = Product.objects.all()
        for item in queryset.iterator():
            code = item.product_code
            category = item.product_category.category_short_name
            url = Product.get_site_url(code, category)
            item.product_site_url = url
            item.save()
            print(item.product_code, item.product_site_url)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
