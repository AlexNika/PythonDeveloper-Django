import os
import numpy as np
import pandas as pd
from django.db import models
from django.urls import reverse

from .constants import product_code_col, product_index_col, product_eancode_col, product_brand_col
from .constants import product_category_col, product_status_col
from .constants import true_ext, brand, category_dict


class Category(models.Model):
    category_short_name = models.CharField(max_length=10, unique=True)
    category_name = models.CharField(max_length=64, unique=True)
    category_description = models.CharField(max_length=256, null=True, blank=True)
#    category_url = models.SlugField(max_length=256, unique=True)
    objects = models.Manager()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_code = models.CharField(max_length=16, blank=True, null=True)
    product_index = models.PositiveIntegerField(unique=True)
    product_eancode = models.CharField(max_length=16, unique=True)
    active_Z1 = 'Z1'
    active_ZN = 'ZN'
    active_Z9 = 'Z9'
    sellout_SZ = 'SZ'
    archive_WS = 'WS'
    status_choices = [
        (active_Z1, 'Z1'),
        (active_ZN, 'ZN'),
        (active_Z9, 'Z9'),
        (archive_WS, 'WS'),
        (sellout_SZ, 'SZ'),
    ]
    product_status = models.CharField(max_length=2,
                                      choices=status_choices,
                                      default=active_Z9, blank=True, null=True)
    product_description = models.CharField(max_length=128, blank=True, null=True)
    product_site_url = models.URLField(max_length=128, blank=True, null=True)
    product_ftp_url = models.URLField(max_length=128, blank=True, null=True)
    product_category = models.ForeignKey(Category, on_delete=models.PROTECT)
    objects = models.Manager()

    class Meta:
        ordering = ["product_code"]

    def __str__(self):
        return self.product_code

    def get_absolute_url(self):
        return reverse("core_app:product_detail", kwargs={"slug": self.product_index})

    def full_code(self):
        return f'{self.product_code}.{str(self.product_index)}.{self.product_eancode}'

    @staticmethod
    def xls_parse(file_name):
        ext = os.path.splitext(str(file_name))[1]
        if ext in true_ext:
            if ext == true_ext[0]:
                df = pd.read_excel(file_name)
                df[product_eancode_col].replace('', np.nan, inplace=True)
                df.dropna(subset=[product_eancode_col], inplace=True)
                for _, row in df.iterrows():
                    if row[product_brand_col] == brand[1]:
                        if row[product_index_col].isdigit():
                            product = Product()
                            product.product_index = row[product_index_col]
                            product.product_code = row[product_code_col].strip().replace(' ', '')
                            product.product_eancode = str(int(row[product_eancode_col]))
                            if [product_status_col] == np.nan:
                                product.product_status = ''
                            else:
                                product.product_status = row[product_status_col]
                            try:
                                category = Category.objects.get(category_short_name=row[product_category_col])
                                product.product_category = category
                                product.product_description = Product.description_gen(row[product_code_col],
                                                                                      row[product_category_col])
                            except Category.DoesNotExist:
                                continue
                            product.save()

    @staticmethod
    def description_gen(code, category):
        description = f'{category_dict[category][0]} {brand[0]} {code}'
        return description


class Content(models.Model):
    pass
