from rest_framework import routers
from core_app.api.views import CategoriesAPIListView, ProductsAPIListView


class Router(routers.DefaultRouter):

    def get_api_root_view(self, api_urls=None):
        root_view = super(Router, self).get_api_root_view(api_urls=api_urls)
        root_view.cls.__doc__ = 'Place your documentation here'
        root_view.cls.__name__ = 'Hansa Content Library Api v.0'
        return root_view


router = Router()
router.register(r'categories', CategoriesAPIListView)
router.register(r'products', ProductsAPIListView)

