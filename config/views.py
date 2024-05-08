from django.shortcuts import render, redirect
from E_Shop.models import Product

def BASE(request):
    return render(request, 'main/base.html')

def HOME(request):
    product = Product.objects.all()

    context = {
        'product': product,
        
    }
    return render(request, 'main/index.html')