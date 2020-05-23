from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from core_app.constants import BASE_GOODS_FILE_NAME, BASE_MRKTD_FILE_NAME, BASE_PRICE_FILE_NAME
from core_app.models import Product
from .forms import FileForm
from .models import File


@login_required
@cache_page(0)
def import_file(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            form = FileForm()
            return render(request, 'file_parser_app/import_XLSX_file.html', context={'form': form})
        else:
            form = FileForm(request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                file_name = form.cleaned_data['file_name']
                file = File.objects.last()
                if FileForm.get_filename(file_name) == BASE_GOODS_FILE_NAME:
                    Product.xls_parse1(file.file_name)
                elif FileForm.get_filename(file_name) == BASE_MRKTD_FILE_NAME:
                    Product.xls_parse2(file.file_name)
                else:
                    pass
                return render(request, 'file_parser_app/import_XLSX_file.html',
                              context={'form': form, 'file_name': file_name})
            else:
                return render(request, 'file_parser_app/import_XLSX_file.html', context={'form': form})
