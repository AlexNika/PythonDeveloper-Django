from django.shortcuts import render

from core_app.models import Product
from core_app.views import CategoryContextMixin, StatusContextMixin
from .forms import FileForm
from .models import File


def import_file(request):
    is_loaded = False
    if request.method == 'GET':
        form = FileForm()
        return render(request, 'file_parser_app/import_XLSX_file.html', context={'form': form})
    else:
        form = FileForm(request.POST, files=request.FILES)
        if form.is_valid():
            file_name = form.cleaned_data.get('file_name')
            form.save()
            is_loaded = True
            file = File.objects.last()
            Product.xls_parse(file.file_name)
            return render(request, 'file_parser_app/import_XLSX_file.html',
                          context={'form': form, 'is_loaded': is_loaded, 'file_name': file_name})
        else:
            file_name = form.cleaned_data.get('file_name')
            return render(request, 'file_parser_app/import_XLSX_file.html',
                          context={'form': form, 'is_loaded': is_loaded, 'file_name': file_name})
