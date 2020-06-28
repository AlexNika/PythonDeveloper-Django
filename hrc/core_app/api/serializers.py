from rest_framework import serializers
from core_app.models import Category, Product


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Category
        fields = ['id',
                  'url',
                  'category_short_name',
                  'category_name',
                  'category_description',
                  'category_site_url',
                  'category_image',
                  'user_id',
                  'is_active']
        lookup_field = 'category_short_name'
        extra_kwargs = {
            'url': {'lookup_field': 'category_short_name'}
        }


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    product_category_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Product
        fields = ['id',
                  'url',
                  'product_index',
                  'product_code',
                  'product_eancode',
                  'product_status',
                  'product_description',
                  'marketing_description',
                  'product_category_id',
                  'product_site_url',
                  'product_internal_path',
                  'product_external_url',
                  'user_id',
                  'is_active']
        lookup_field = 'product_code'
        extra_kwargs = {
            'url': {'lookup_field': 'product_code'}
        }
