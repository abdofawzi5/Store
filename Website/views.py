from django.shortcuts import render
from Company.models import Company
from Website.models import Message, Advertisement
from Product.views import allProductWithCategory
import json 

def index(request):
    context = {}
    context['company'] = Company.objects.all()[0]
    return render(request, 'website/index.html',context)

def products(request):
    context = {}
    context['company'] = Company.objects.all()[0]
    context['ads'] = Advertisement.objects.all()
    context['categories'] = allProductWithCategory()
    return render(request, 'website/products.html',context)

def contanct(request):
    try:
        fullName = request.GET.get('name')
        phone = request.GET.get('phone')
        email = request.GET.get('email')
        message = request.GET.get('message')
        if fullName and phone and email and message:
            msg = Message(name=fullName,email=email,phone=phone,message=message)
            msg.save()
    except:
        pass
    context = {}
    context['company'] = Company.objects.all()[0]
    return render(request, 'website/contact.html',context)
