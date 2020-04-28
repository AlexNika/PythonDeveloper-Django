from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core_app.models import Product
from .forms import FileForm
from .models import File


@login_required
def import_file(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            form = FileForm()
            return render(request, 'file_parser_app/import_XLSX_file.html', context={'form': form})
        else:
            form = FileForm(request.POST, files=request.FILES)
            if form.is_valid():
                file_name = form.cleaned_data.get('file_name')
                form.save()
                file = File.objects.last()
                Product.xls_parse(file.file_name)
                return render(request, 'file_parser_app/import_XLSX_file.html',
                              context={'form': form, 'file_name': file_name})
            else:
                file_name = form.cleaned_data.get('file_name')
                return render(request, 'file_parser_app/import_XLSX_file.html',
                              context={'form': form, 'file_name': file_name})
