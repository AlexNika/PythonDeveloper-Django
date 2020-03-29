from django.urls import path
from file_parser_app import views

app_name = 'file_parser_app'

urlpatterns = [
    path('import_files/', views.import_file, name='import_file'),
]
