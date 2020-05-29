from django.contrib import admin
from django.contrib.admin import AdminSite
from reversion.admin import VersionAdmin
from .models import Category, Product


class CategoryAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('category_short_name', 'category_name', 'category_description', 'is_active')
    actions = ['set_active', 'set_inactive']
    ordering = ['category_short_name', 'category_name', 'is_active']

    def set_active(self, request, queryset):
        queryset.update(is_active=True)
    set_active.short_description = 'Mark selected categories as active'

    def set_inactive(self, request, queryset):
        queryset.update(is_active=False)
    set_inactive.short_description = 'Mark selected categories as inactive'

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(CategoryAdmin, self).save_model(request, obj, form, change)


class ProductAdmin(VersionAdmin, admin.ModelAdmin):
    fields = ('product_code', 'product_index', 'product_eancode', 'product_category',
              'product_status', 'product_description', 'marketing_description', 'product_site_url',
              'product_internal_path', 'product_external_url', 'user', 'is_active', 'rc_complete')
    list_display = ('product_code', 'product_index', 'product_eancode', 'product_category',
                    'product_status', 'is_active')
    list_filter = ('product_status', 'product_category')
    actions = ['set_active', 'set_inactive']
    ordering = ['product_code', 'product_category', 'product_status']
    readonly_fields = ['product_code', 'product_index', 'product_eancode', 'user', 'rc_complete']

    def set_active(self, request, queryset):
        queryset.update(is_active=True)
    set_active.short_description = 'Mark selected products as active'

    def set_inactive(self, request, queryset):
        queryset.update(is_active=False)
    set_inactive.short_description = 'Mark selected products as inactive'

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(ProductAdmin, self).save_model(request, obj, form, change)


class HCLAdminSite(AdminSite):
    site_header = 'Администрирование Hansa Content Library'


admin.site = HCLAdminSite(name='admin')
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
