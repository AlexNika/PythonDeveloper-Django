from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import ContextMixin

from .forms import FeedbackForm, CategoryForm, ProductForm, ProductSiteUrl, CategorySiteUrl
from .models import Category, Product


class CategoryContextMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.select_related().all()
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


class FeedbackView(FormView):
    template_name = 'core_app/feedback.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('core_app:product_list')

    def form_valid(self, form):
        form.send_email()
        return super(FeedbackView, self).form_valid(form)


class CategoryListView(ListView, CategoryContextMixin):
    queryset = Category.objects.select_related()
    template_name = 'core_app/category_list.html'


class CategoryDetailView(DetailView, CategoryContextMixin):
    queryset = Category.objects.select_related()
    slug_field = 'category_short_name'
    template_name = 'core_app/category_detail.html'


class CategoryCreateView(LoginRequiredMixin, CreateView, CategoryContextMixin):
    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('core_app:category_list')
    template_name = 'core_app/category_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView, CategoryContextMixin):
    form_class = CategoryForm
    queryset = Category.objects.select_related()
    slug_field = 'category_short_name'
    success_url = reverse_lazy('core_app:category_list')
    template_name = 'core_app/category_update.html'


class CategoryDeleteView(LoginRequiredMixin, DeleteView, CategoryContextMixin):
    model = Category
    success_url = reverse_lazy('core_app:category_list')
    template_name = 'core_app/category_delete_confirm.html'


class ProductListView(ListView, CategoryContextMixin, StatusContextMixin):
    queryset = Product.objects.select_related()
    paginate_by = 15
    context_object_name = 'products'
    form = ProductForm
    template_name = 'core_app/product_list.html'


class ProductDetailView(DetailView, CategoryContextMixin, StatusContextMixin):
    queryset = Product.objects.select_related()
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
    context_object_name = 'product'
    success_url = reverse_lazy('core_app:product_list')
    slug_field = 'product_index'
    template_name = 'core_app/product_update.html'


class SearchFilterProductsView(ListView, CategoryContextMixin, StatusContextMixin):
    model = Product
    paginate_by = 15
    context_object_name = 'products'
    slug_field = 'product_index'
    template_name = 'core_app/product_search_result.html'

    def get_queryset(self):
        sphrase = self.request.GET.get('sphrase')
        status = self.request.GET.get('status')
        category = self.request.GET.get('category')
        if (sphrase == '') and (status != 'all') and (category == 'all'):
            queryset = Product.objects.select_related('product_category').filter(product_status__icontains=status)
            return queryset
        elif (sphrase == '') and (status == 'all') and (category != 'all'):
            queryset = Product.objects.select_related('product_category').filter(
                product_category=Category.objects.get(category_short_name=category).id)
            return queryset
        elif (sphrase == '') and (status != 'all') and (category != 'all'):
            queryset = Product.objects.select_related('product_category').filter(
                Q(product_status__icontains=status),
                Q(product_category=Category.objects.get(category_short_name=category).id))
            return queryset
        elif (sphrase != '') and (status == 'all') and (category == 'all'):
            queryset = Product.objects.select_related('product_category').filter(
                Q(product_index__icontains=sphrase) |
                Q(product_code__icontains=sphrase) |
                Q(product_eancode__icontains=sphrase))
            return queryset
        elif (sphrase != '') and (status != 'all') and (category == 'all'):
            queryset = Product.objects.select_related('product_category').filter(
                Q(product_index__icontains=sphrase) |
                Q(product_code__icontains=sphrase) |
                Q(product_eancode__icontains=sphrase),
                Q(product_status__icontains=status))
            return queryset
        elif (sphrase != '') and (status == 'all') and (category != 'all'):
            queryset = Product.objects.select_related('product_category').filter(
                Q(product_index__icontains=sphrase) |
                Q(product_code__icontains=sphrase) |
                Q(product_eancode__icontains=sphrase),
                Q(product_category=Category.objects.get(category_short_name=category).id))
            return queryset
        elif (sphrase != '') and (status != 'all') and (category != 'all'):
            queryset = Product.objects.select_related('product_category').filter(
                Q(product_index__icontains=sphrase) |
                Q(product_code__icontains=sphrase) |
                Q(product_eancode__icontains=sphrase),
                Q(product_status__icontains=status),
                Q(product_category=Category.objects.get(category_short_name=category).id))
            return queryset
        else:
            queryset = Product.objects.select_related('product_category').all()
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
            url = Product.get_product_site_url(code, category)
            item.product_site_url = url
            item.save()
            print(item.product_code, item.product_site_url)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryUrlFieldFill(LoginRequiredMixin, ListView):
    form_class = CategorySiteUrl
    model = Category
    context_object_name = 'categories'
    success_url = reverse_lazy('core_app:category_list')
    template_name = 'core_app/category_site_url_filling.html'

    def get_queryset(self):
        queryset = Category.objects.all()
        for item in queryset.iterator():
            category = item.category_short_name
            url = Category.get_category_site_url(category)
            item.category_site_url = url
            item.save()
            print(item.category_short_name, item.category_site_url)
        return queryset
