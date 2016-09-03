from django.shortcuts import render
from Company.models import Company

def index(request):
    context = {}
    context['company'] = Company.objects.all()[0]
    return render(request, 'website/index.html',context)

def products(request):
    context = {}
    context['company'] = Company.objects.all()[0]
    return render(request, 'website/products.html',context)

def contanct(request):
    context = {}
    context['company'] = Company.objects.all()[0]
    return render(request, 'website/contact.html',context)

