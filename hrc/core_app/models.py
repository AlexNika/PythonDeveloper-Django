import os
import platform
import subprocess
import time
from tqdm import tqdm

import numpy as np
import pandas as pd
import requests
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.db.utils import IntegrityError

from user_app.models import CoreUser, get_user_auth
from .constants import HEADER
from .constants import brand, brand_url, category_dict
from .constants import int_server_name, ext_server_name, local_file_dir
from .constants import product_category_col, product_status_col, marketing_description_col
from .constants import product_code_col, product_index_col, product_eancode_col, product_brand_col


def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0


def network_root_path():
    return os.path.join('\\\\', int_server_name, '\\')


def server_is_available(direction):
    if direction == 'internal':
        if ping(int_server_name):
            return True
        else:
            return False
    elif direction == 'external':
        if ping(ext_server_name):
            return True
        else:
            return False


class TimeStamp(models.Model):
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStamp):
    category_short_name = models.CharField(max_length=10, unique=True, db_index=True)
    category_name = models.CharField(max_length=64, unique=True)
    category_description = models.CharField(max_length=256, null=True, blank=True)
    category_site_url = models.URLField(max_length=128, blank=True, null=True)
    category_image = models.ImageField(upload_to='categories', blank=True, null=True)
    user = models.ForeignKey(CoreUser, on_delete=models.PROTECT, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name

    def has_image(self):
        return bool(self.category_image)

    def get_absolute_url(self):
        return reverse("core_app:category_detail", kwargs={"slug": self.category_short_name})

    @staticmethod
    def get_category_site_url(category):
        time.sleep(1)
        url = f'{brand_url}catalog/{category_dict[category][2]}/'
        url_request = requests.get(url, headers=HEADER)
        if url_request.status_code == 200:
            return url
        else:
            return None


class Product(TimeStamp):
    product_code = models.CharField(max_length=16, blank=True, null=True, db_index=True)
    product_index = models.PositiveIntegerField(unique=True, db_index=True)
    product_eancode = models.CharField(max_length=16, unique=True, db_index=True)
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
    product_status = models.CharField(max_length=5,
                                      choices=status_choices,
                                      default=active_Z9, blank=True, null=True, db_index=True)
    product_description = models.CharField(max_length=128, blank=True, null=True)
    marketing_description = models.TextField(blank=True)
    product_site_url = models.URLField(max_length=128, blank=True, null=True)
    product_internal_path = models.URLField(max_length=128, blank=True, null=True)
    product_external_url = models.URLField(max_length=128, blank=True, null=True)
    product_category = models.ForeignKey(Category, on_delete=models.PROTECT, db_index=True)
    user = models.ForeignKey(CoreUser, on_delete=models.PROTECT, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    rc_complete = models.PositiveSmallIntegerField(default=0)
    objects = models.Manager()

    class Meta:
        ordering = ["product_code"]

    def __str__(self):
        return self.product_code

    def get_absolute_url(self):
        return reverse("core_app:product_detail", kwargs={"slug": self.product_index})

    def get_full_code(self):
        if self.product_code and self.product_index and self.product_eancode:
            return f'{self.product_code}.{str(self.product_index)}.{self.product_eancode}'
        return None

    def is_exist_internal_path(self):
        if self.product_internal_path:
            return os.path.exists(self.product_internal_path)
        else:
            return None

    def create_folders_structure(self, where):
        if server_is_available(where):
            self.where = where
            full_code = self.get_full_code()
            middle_part_path = category_dict[self.product_category.category_short_name][1]
            path = f'\\\\{int_server_name}\\{local_file_dir}'
            if self.where == 'internal':
                user_config = get_user_auth()
                command = f'net use Z: {path} {user_config["user_password"]} /user:{user_config["user_login"]} ' \
                          f'/persistent:no'
                subprocess.call(command, shell=True)
                try:
                    os.chdir('Z:\\')
                    os.chdir(middle_part_path)
                    os.mkdir(path)
                except FileExistsError:
                    print(f'Folder {full_code} already exists!')

    # def save(self, *args, **kwargs):
    #     super(Product, self).save(*args, **kwargs)
    #     # self.create_folders_structure('internal')

    @staticmethod
    def xls_parse1(file_name):
        df = pd.read_excel(file_name)
        df[product_eancode_col].replace('', np.nan, inplace=True)
        df.dropna(subset=[product_eancode_col], inplace=True)
        pbar = tqdm(total=len(df.index))
        for _, row in df.iterrows():
            if row[product_brand_col] == brand[1] or row[product_eancode_col] != '':
                if str(row[product_index_col]).isdigit():
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
                        product.product_site_url = Product.get_product_site_url(row[product_code_col],
                                                                                row[product_category_col])
                    except Category.DoesNotExist:
                        continue
                    try:
                        product.save()
                    except IntegrityError:
                        continue
            pbar.update(n=1)
        pbar.close()

    @staticmethod
    def xls_parse2(file_name):
        # парсинг файла маркетинговых описаний и заполнение поля marketing_description модели Product
        df = pd.read_excel(file_name)
        pbar = tqdm(total=len(df.index))
        for _, row in df.iterrows():
            query_product_code = row[product_code_col].strip().replace(' ', '')
            query_product_index = row[product_index_col]
            Product.objects.filter(
                Q(product_code=query_product_code),
                Q(product_index=query_product_index)).update(
                marketing_description=' '.join(row[marketing_description_col].split()))
            pbar.update(n=1)
        pbar.close()

    @staticmethod
    def description_gen(code, category):
        description = f'{category_dict[category][0]} {brand[0]} {code}'
        return description

    @staticmethod
    def get_product_site_url(code, category):
        time.sleep(1)
        _dot = '.'
        _dash = '-'
        _gap = ' '
        code = code.lower()
        if _dot in code:
            code = code.replace(_dot, _dash)
        elif _gap in code:
            code = code.replace(_gap, '')
        url = f'{brand_url}catalog/{category_dict[category][2]}/{code}/'
        url_request = requests.get(url, headers=HEADER)
        if url_request.status_code == 200:
            return url
        else:
            return None


class Content(TimeStamp):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True
        # primary_key=True,
        # default=Product.get_new,
    )
    layout = models.BooleanField(default=False)
    layout_internal_path = models.FilePathField(path=network_root_path, recursive=True,
                                                allow_folders=True, max_length=256, null=True, blank=True)
    layout_external_url = models.URLField(max_length=128, blank=True, null=True)
    layout_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    maquette = models.BooleanField(default=False)
    maquette_internal_path = models.FilePathField(path=network_root_path, recursive=True,
                                                  allow_folders=True, max_length=256, null=True, blank=True)
    maquette_external_url = models.URLField(max_length=128, blank=True, null=True)
    maquette_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    photos = models.BooleanField(default=False)
    photos_internal_path = models.FilePathField(path=network_root_path, recursive=True,
                                                allow_folders=True, max_length=256, null=True, blank=True)
    photos_external_url = models.URLField(max_length=128, blank=True, null=True)
    photos_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    photos_3d = models.BooleanField(default=False)
    photos_3d_internal_path = models.FilePathField(path=network_root_path, recursive=True,
                                                   allow_folders=True, max_length=256, null=True, blank=True)
    photos_3d_external_url = models.URLField(max_length=128, blank=True, null=True)
    photos_3d_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    interior_photos = models.BooleanField(default=False)
    interior_photos_internal_path = models.FilePathField(path=network_root_path, recursive=True,
                                                         allow_folders=True, max_length=256, null=True, blank=True)
    interior_photos_external_url = models.URLField(max_length=128, blank=True, null=True)
    interior_photos_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    auxiliary_photos = models.BooleanField(default=False)
    auxiliary_photos_internal_path = models.FilePathField(path=network_root_path, recursive=True,
                                                          allow_folders=True, max_length=256, null=True, blank=True)
    auxiliary_photos_external_url = models.URLField(max_length=128, blank=True, null=True)
    auxiliary_photos_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    manuals = models.BooleanField(default=False)
    manuals_internal_path = models.FilePathField(path=network_root_path, recursive=True,
                                                 allow_folders=True, max_length=256, null=True, blank=True)
    manuals_external_url = models.URLField(max_length=128, blank=True, null=True)
    manuals_photos_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    videos = models.BooleanField(default=False)
    videos_internal_path = models.FilePathField(path=network_root_path, recursive=True,
                                                allow_folders=True, max_length=256, null=True, blank=True)
    videos_external_url = models.URLField(max_length=128, blank=True, null=True)
    videos_photos_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    descriptions = models.BooleanField(default=False)
    descriptions_internal_path = models.FilePathField(path=network_root_path, recursive=True,
                                                      allow_folders=True, max_length=256, null=True, blank=True)
    descriptions_external_url = models.URLField(max_length=128, blank=True, null=True)
    descriptions_photos_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    characteristics = models.BooleanField(default=False)
    characteristics_internal_path = models.FilePathField(path=network_root_path, recursive=True,
                                                         allow_folders=True, max_length=256, null=True, blank=True)
    characteristics_external_url = models.URLField(max_length=128, blank=True, null=True)
    characteristics_photos_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    user = models.ForeignKey(CoreUser, on_delete=models.PROTECT, blank=True, null=True)
    objects = models.Manager()
