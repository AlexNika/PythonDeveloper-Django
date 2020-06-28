import os
import platform
import string
import subprocess
import time

import numpy as np
import pandas as pd
import requests
from django.db import models
from django.db.models import Q
from django.db.utils import IntegrityError
from django.urls import reverse
from tqdm import tqdm

from user_app.models import CoreUser, get_user_auth
from .constants import HEADER
from .constants import brand, brand_url, category_dict
from .constants import int_server_name, ext_server_name
from .constants import product_category_col, product_status_col, marketing_description_col
from .constants import product_code_col, product_index_col, product_eancode_col, product_brand_col
from .managers import ActiveManager


class IsActiveMixin(models.Model):
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True


def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command, stdout=subprocess.DEVNULL) == 0


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


def site_is_available():
    url = f'{brand_url}/'
    url_request = requests.get(url, headers=HEADER)
    if url_request.status_code == 200:
        return True
    else:
        return False


def int_srv_connect(where, path):
    if server_is_available(where):
        user_config = get_user_auth()
        command = f'net use Z: "{path}" {user_config["user_password"]} /user:{user_config["user_login"]} ' \
                  f'/persistent:no'
        subprocess.call(command, shell=True)


def available_drives():
    return [f'{d}:' for d in string.ascii_uppercase if os.path.exists(f'{d}:')]


class TimeStamp(models.Model):
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStamp, IsActiveMixin):
    category_short_name = models.CharField(max_length=10, unique=True, db_index=True)
    category_slug = models.SlugField(max_length=10, null=True, blank=True, db_index=True)
    category_name = models.CharField(max_length=64, unique=True)
    category_description = models.CharField(max_length=256, null=True, blank=True)
    category_site_url = models.URLField(max_length=128, blank=True, null=True)
    category_image = models.ImageField(upload_to='categories', blank=True, null=True)
    user = models.ForeignKey(CoreUser, on_delete=models.PROTECT, blank=True, null=True)
    objects = models.Manager()
    active_objects = ActiveManager()

    class Meta:
        default_manager_name = 'objects'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.category_slug = self.category_short_name.lower().replace('.', '-')
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name

    def has_image(self):
        return bool(self.category_image)

    def get_absolute_url(self):
        return reverse("core_app:category_detail", kwargs={"slug": self.category_slug})

    @staticmethod
    def get_site_url(category):
        time.sleep(1)
        url = f'{brand_url}catalog/{category_dict[category][2]}/'
        url_request = requests.get(url, headers=HEADER)
        if url_request.status_code == 200:
            return url
        else:
            return ''


class Product(TimeStamp, IsActiveMixin):
    product_code = models.CharField(max_length=16, blank=True, null=True, db_index=True)
    product_slug = models.SlugField(max_length=16, blank=True, null=True, db_index=True, allow_unicode=True)
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
    product_internal_path = models.CharField(max_length=128, blank=True, null=True)
    product_external_url = models.URLField(max_length=128, blank=True, null=True)
    product_category = models.ForeignKey(Category, on_delete=models.PROTECT, db_index=True)
    user = models.ForeignKey(CoreUser, on_delete=models.PROTECT, blank=True, null=True)
    rc_complete = models.PositiveSmallIntegerField(default=0)
# -------
    layout = models.BooleanField(default=False)
    layout_internal_path = models.CharField(max_length=256, null=True, blank=True)
    layout_external_url = models.URLField(max_length=128, blank=True, null=True)
    layout_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    maquette = models.BooleanField(default=False)
    maquette_internal_path = models.CharField(max_length=256, null=True, blank=True)
    maquette_external_url = models.URLField(max_length=128, blank=True, null=True)
    maquette_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    photos = models.BooleanField(default=False)
    photos_internal_path = models.CharField(max_length=256, null=True, blank=True)
    photos_external_url = models.URLField(max_length=128, blank=True, null=True)
    photos_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    photos_3d = models.BooleanField(default=False)
    photos_3d_internal_path = models.CharField(max_length=256, null=True, blank=True)
    photos_3d_external_url = models.URLField(max_length=128, blank=True, null=True)
    photos_3d_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    interior_photos = models.BooleanField(default=False)
    interior_photos_internal_path = models.CharField(max_length=256, null=True, blank=True)
    interior_photos_external_url = models.URLField(max_length=128, blank=True, null=True)
    interior_photos_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    auxiliary_photos = models.BooleanField(default=False)
    auxiliary_photos_internal_path = models.CharField(max_length=256, null=True, blank=True)
    auxiliary_photos_external_url = models.URLField(max_length=128, blank=True, null=True)
    auxiliary_photos_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    manuals = models.BooleanField(default=False)
    manuals_internal_path = models.CharField(max_length=256, null=True, blank=True)
    manuals_external_url = models.URLField(max_length=128, blank=True, null=True)
    manuals_photos_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    videos = models.BooleanField(default=False)
    videos_internal_path = models.CharField(max_length=256, null=True, blank=True)
    videos_external_url = models.URLField(max_length=128, blank=True, null=True)
    videos_photos_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    descriptions = models.BooleanField(default=False)
    descriptions_internal_path = models.CharField(max_length=256, null=True, blank=True)
    descriptions_external_url = models.URLField(max_length=128, blank=True, null=True)
    descriptions_photos_folder_hash = models.CharField(max_length=256, blank=True, null=True)
    characteristics = models.BooleanField(default=False)
    characteristics_internal_path = models.CharField(max_length=256, null=True, blank=True)
    characteristics_external_url = models.URLField(max_length=128, blank=True, null=True)
    characteristics_photos_folder_hash = models.CharField(max_length=256, blank=True, null=True)
# -------
    objects = models.Manager()
    active_objects = ActiveManager()

    class Meta:
        ordering = ["product_code"]

    def save(self, *args, **kwargs):
        self.product_slug = self.product_code.lower().replace('.', '-')
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_code

    def get_absolute_url(self):
        return reverse("core_app:product_detail", kwargs={"slug": self.product_slug})

    def get_full_code(self):
        if self.product_code and self.product_index and self.product_eancode:
            return f'{self.product_code}.{str(self.product_index)}.{self.product_eancode}'
        return None

    def is_exist_internal_path(self):
        if self.product_internal_path:
            return os.path.exists(self.product_internal_path)
        else:
            return None

    # def create_folders_structure(self, where):
    #     if server_is_available(where):
    #         full_code = self.get_full_code()
    #         middle_part_path = category_dict[self.product_category.category_short_name][1]
    #         path = f'\\\\{int_server_name}\\{local_file_dir}'
    #         if where == 'internal':
    #             int_srv_connect(where, path)
    #             try:
    #                 os.chdir('Z:\\')
    #                 os.chdir(middle_part_path)
    #                 os.mkdir(path)
    #             except FileExistsError:
    #                 print(f'Folder {full_code} already exists!')

    @staticmethod
    def get_folders(initial_path, depth):
        if server_is_available('internal'):
            if 'Z:' not in available_drives():
                int_srv_connect('internal', initial_path)
        else:
            return None
        folders = {}
        tail = os.path.split(initial_path)[-1]
        with os.scandir(initial_path) as tree1:
            for item1 in tree1:
                if not item1.is_file():
                    if depth == 0:
                        if tail in folders:
                            folders[tail].append(item1.name)
                        else:
                            folders[tail] = [item1.name]
                    else:
                        with os.scandir(item1) as tree2:
                            for item2 in tree2:
                                if not item2.is_file():
                                    if item1.name in folders:
                                        try:
                                            folders[item1.name].append(item2.name)
                                        except AttributeError:
                                            folders[item1.name] = [folders[item1.name], item2.name]
                                    else:
                                        folders[item1.name] = item2.name
        return folders

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
                        product.product_site_url = Product.get_site_url(row[product_code_col],
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
    def get_site_url(code, category):
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
            return ''
