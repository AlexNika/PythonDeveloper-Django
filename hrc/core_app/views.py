import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import ContextMixin
from tqdm import tqdm

from .constants import int_server_name, local_file_dir, category_dict, brand_url, predefined_folders
from .forms import FeedbackForm, CategoryForm, ProductForm, ProductSiteUrl, CategorySiteUrl
from .models import Category, Product, site_is_available, server_is_available


def handler404(request, exception):
    context = {}
    response = render(request, "core_app/404.html", context=context)
    response.status_code = 404
    return response


def handler50x(request):
    context = {}
    response = render(request, "core_app/500.html", context=context)
    response.status_code = 500
    return response


def unwrap_list(mylist, result):
    if any(isinstance(i, list) for i in mylist):
        for value in mylist:
            unwrap_list(value, result)
    else:
        result.append(mylist)


class CategoryContextMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.select_related().filter(is_active=True)
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
    template_name = 'core_app/category_list.html'

    def get_queryset(self):
        queryset = Category.active_objects.select_related().all()
        return queryset


class CategoryDetailView(DetailView, CategoryContextMixin):
    queryset = Category.objects.select_related()
    slug_field = 'category_slug'
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
    slug_field = 'category_slug'
    success_url = reverse_lazy('core_app:category_list')
    template_name = 'core_app/category_update.html'


class CategoryDeleteView(LoginRequiredMixin, DeleteView, CategoryContextMixin):
    model = Category
    success_url = reverse_lazy('core_app:category_list')
    template_name = 'core_app/category_delete_confirm.html'


class ProductListView(ListView, CategoryContextMixin, StatusContextMixin):
    paginate_by = 15
    context_object_name = 'products'
    form = ProductForm
    template_name = 'core_app/product_list.html'

    def get_queryset(self):
        queryset = Product.objects.select_related().filter(is_active=True, product_category__is_active=True)
        return queryset


class ProductDetailView(DetailView):
    queryset = Product.objects.select_related()
    context_object_name = 'product'
    slug_field = 'product_slug'
    template_name = 'core_app/product_detail.html'


class ProductCreateView(LoginRequiredMixin, CreateView, CategoryContextMixin, StatusContextMixin):
    form_class = ProductForm
    model = Product
    success_url = reverse_lazy('core_app:product_list')
    template_name = 'core_app/product_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProductCreateView, self).form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProductForm
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('core_app:product_list')
    slug_field = 'product_slug'
    template_name = 'core_app/product_update.html'


class SearchFilterProductsView(ListView, CategoryContextMixin, StatusContextMixin):
    model = Product
    paginate_by = 15
    context_object_name = 'products'
    slug_field = 'product_slug'
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


class CategoryProcessor(LoginRequiredMixin, ListView):
    form_class = CategorySiteUrl
    model = Category
    context_object_name = 'categories'
    template_name = 'core_app/category_processor.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        alert_category = False
        form = self.form_class(request.POST)
        if site_is_available():
            queryset = self.get_queryset()
            if 'process_1' in self.request.POST:
                pbar = tqdm(total=len(queryset))
                for item in queryset.iterator():
                    category = item.category_short_name
                    url = Category.get_site_url(category)
                    item.category_site_url = url
                    item.save()
                    pbar.update(n=1)
                pbar.close()
            else:
                return render(request, self.template_name, {'form': form})
        else:
            alert_category = True
            return render(request, self.template_name,
                          {'form': form, 'alert_category': alert_category, 'site': brand_url})
        return HttpResponseRedirect('/categories/')

    def get_queryset(self):
        queryset = Category.objects.select_related().all()
        return queryset


class ProductProcessor(LoginRequiredMixin, ListView):
    form_class = ProductSiteUrl
    model = Product
    context_object_name = 'products'
    template_name = 'core_app/product_processor.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        alert_product = False
        form = self.form_class(request.POST)
        if form.is_valid():
            queryset = self.get_queryset()
            path_start = os.path.join('\\\\', int_server_name, local_file_dir)
            if 'process_3' in self.request.POST:
                folders = Product.get_folders(path_start, 1)
                if folders is None:
                    alert_product = True
                    return render(request, self.template_name,
                                  {'form': form, 'alert_product': alert_product, 'srv': int_server_name})
                folders_values = []
                pbar = tqdm(total=len(queryset))
                for key in folders:
                    folders_values += list(folders[key])
                for item in queryset.iterator():
                    path_middle = category_dict[item.product_category.category_short_name][1]
                    path_end = item.get_full_code()
                    product_internal_path = os.path.join(path_start, path_middle, path_end)
                    if path_end in folders_values:
                        item.product_internal_path = product_internal_path
                        item.save()
                    pbar.update(n=1)
                pbar.close()
            elif 'process_2' in self.request.POST:
                if site_is_available():
                    pbar = tqdm(total=len(queryset))
                    for item in queryset.iterator():
                        code = item.product_code
                        category = item.product_category.category_short_name
                        site_url = Product.get_site_url(code, category)
                        item.product_site_url = site_url
                        item.save()
                        pbar.update(n=1)
                    pbar.close()
                else:
                    alert_product = True
                    return render(request, self.template_name,
                                  {'form': form, 'alert_product': alert_product, 'site': brand_url})
            elif 'process_4' in self.request.POST:
                if not server_is_available('internal'):
                    alert_product = True
                    return render(request, self.template_name,
                                  {'form': form, 'alert_product': alert_product, 'srv': int_server_name})
                pbar = tqdm(total=len(queryset))
                for item in queryset.iterator():
                    item.rc_complete = 0
                    if not item.product_internal_path:
                        item.rc_complete = 0
                    else:
                        folders = Product.get_folders(item.product_internal_path, 0)
                        if folders is None:
                            continue
                        folders_list = folders.popitem()[-1]
                        for folder in folders_list:
                            path = os.path.join(item.product_internal_path, folder)
                            fn = predefined_folders.get(folder)
                            content_is_exists = os.listdir(path)
                            if not content_is_exists:
                                continue
                            if fn == 1 and content_is_exists:
                                item.layout = True
                                item.layout_internal_path = path
                                item.rc_complete += 10
                            elif fn == 2 and content_is_exists:
                                item.maquette = True
                                item.maquette_internal_path = path
                                item.rc_complete += 10
                            elif fn == 3 and content_is_exists:
                                item.videos = True
                                item.videos_internal_path = path
                                item.rc_complete += 10
                            elif fn == 4 and content_is_exists:
                                item.manuals = True
                                item.manuals_internal_path = path
                                item.rc_complete += 10
                            elif fn == 5 and content_is_exists:
                                item.descriptions = True
                                item.descriptions_internal_path = path
                                item.rc_complete += 10
                            elif fn == 6 and content_is_exists:
                                item.photos_3d = True
                                item.photos_3d_internal_path = path
                                item.rc_complete += 10
                            elif fn == 7 and content_is_exists:
                                item.interior_photos = True
                                item.interior_photos_internal_path = path
                                item.rc_complete += 10
                            elif fn == 8 and content_is_exists:
                                item.auxiliary_photos = True
                                item.auxiliary_photos_internal_path = path
                                item.rc_complete += 10
                            elif fn == 9 and content_is_exists:
                                item.photos = True
                                item.photos_internal_path = path
                                item.rc_complete += 10
                            elif fn == 10 and content_is_exists:
                                item.characteristics = True
                                item.characteristics_internal_path = path
                                item.rc_complete += 10
                            elif fn == 11 and content_is_exists:
                                pass
                    item.save()
                    pbar.update(n=1)
                pbar.close()
            return HttpResponseRedirect('/')

    def get_queryset(self):
        queryset = Product.objects.select_related().all()
        return queryset


# class ContentDetailView(LoginRequiredMixin, DetailView):
#     form_class = ContentDetailForm
#     model = Content
#     context_object_name = 'content'
#     success_url = reverse_lazy('core_app:content_detail')
#     # slug_field = 'product'
#     queryset = Product.objects.get(id=Content.product)
#     slug_field = queryset.values('product_index')
#     print(slug_field)
#     template_name = 'core_app/content_detail.html'

