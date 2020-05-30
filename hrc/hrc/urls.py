from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core_app.api.routers import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core_app.urls', namespace='core_app')),
    path('', include('file_parser_app.urls', namespace='file_parser_app')),
    path('', include('user_app.urls', namespace='user_app')),
    path('api-auth/', include('rest_framework.urls', namespace='api-auth')),
    path('api/v0/', include(router.urls))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
