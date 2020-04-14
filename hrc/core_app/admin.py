from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_short_name', 'category_name', 'category_description',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
