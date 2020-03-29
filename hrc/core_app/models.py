from django.db import models


class Category(models.Model):
    category_short_name = models.CharField(max_length=10, unique=True)
    category_name = models.CharField(max_length=64, unique=True)
    category_description = models.CharField(max_length=256, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_code = models.CharField(max_length=16, unique=True)
    product_index = models.PositiveIntegerField(unique=True)
    product_eancode = models.CharField(max_length=16, unique=True)
    active = 'AC'
    archive = 'AR'
    sellout = 'SO'
    status_choices = [
        (active, 'Active'),
        (archive, 'Archive'),
        (sellout, 'Sell out'),
    ]
    product_status = models.CharField(max_length=2,
                                      choices=status_choices,
                                      default=active, unique=True)
    product_description = models.CharField(max_length=64, unique=True)
    product_site_url = models.URLField(max_length=128)
    product_ftp_url = models.URLField(max_length=128)
    product_category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.product_code

    def full_code(self):
        return f'{self.product_code}.{str(self.product_index)}.{self.product_eancode}'
