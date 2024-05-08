from django.shortcuts import render, redirect
from E_Shop.models import Product

def BASE(request):
    return render(request, 'main/base.html')

def HOME(request):
    product = Product.objects.filter(status = 'Publish')

    context = {
        'product': product,
    }

    return render(request, 'main/index.html', context)

def PRODUCT(request):
    product = Product.objects.filter(status = 'Publish')

    context = {
        'product': product,
    }
    
    return render(request, 'main/product.html',context)