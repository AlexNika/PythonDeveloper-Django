from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from .models import Category
from .forms import ContactForm, CategoryForm


def main_view(request):
    pass
    return render(request, 'core_app/index.html', context={})


def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = f'Сообщение с портара Hansa Rich Content от {name}'
            send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email],
                      fail_silently=True)
            return HttpResponseRedirect(reverse('core_app:main'))
        else:
            return render(request, 'core_app/contacts.html', context={'form': form})
    else:
        form = ContactForm()
        return render(request, 'core_app/contacts.html', context={'form': form})


def create_category(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        form = CategoryForm()
        return render(request, 'core_app/create_category.html', context={'categories': categories, 'form': form})
    else:
        categories = Category.objects.all()
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'core_app/create_category.html', context={'categories': categories, 'form': form})
        else:
            return render(request, 'core_app/create_category.html', context={'categories': categories, 'form': form})
