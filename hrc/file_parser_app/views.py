from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from .models import File
from .forms import FileForm


def import_file(request):
    if request.method == 'GET':
        form = FileForm()
        return render(request, 'file_parser_app/import_SAPGOODS_file.html', context={'form': form})
    else:
        files = File.objects.all()
        form = FileForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'file_parser_app/notification_success.html')
        else:
            return render(request, 'file_parser_app/notification_failed.html')
