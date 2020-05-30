from rest_framework import routers
from core_app.api.views import CategoriesAPIListView, ProductsAPIListView

router = routers.DefaultRouter()
router.register(r'categories', CategoriesAPIListView)
router.register(r'products', ProductsAPIListView)
