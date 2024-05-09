# type: ignore
from django.shortcuts import render, redirect
from E_Shop.models import Product, Categoires, Filter_Price, Color, Brand

def BASE(request):
    return render(request, 'main/base.html')

def HOME(request):
    product = Product.objects.filter(status = 'Publish')

    context = {
        'product': product,
    }

    return render(request, 'main/index.html', context)

def PRODUCT(request):
    product = Product.objects.all()
    categories = Categoires.objects.all()
    filter_price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()

    CATID = request.GET.get('categories')
    PRICE_FILTER_ID = request.GET.get('filter_price')
    COLORID = request.GET.get('color')
    BRANDID = request.GET.get('brand')
    
    
    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')
    
    PRICE_LOWTOHIGHID = request.GET.get('PRICE_LOWTOHIGH')
    PRICE_HIGHTOLOWID = request.GET.get('PRICE_HIGHTOLOW')
    
    NEW_PRODUCTID = request.GET.get('NEW_PRODUCT')
    OLD_PRODUCTID = request.GET.get('OLD_PRODUCT')
    
    
    if CATID:
        product = Product.objects.filter(categories = CATID, status = 'Publish')
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price = PRICE_FILTER_ID, status = 'Publish')
    elif COLORID:
        product = Product.objects.filter(color = COLORID, status = 'Publish')
    elif BRANDID:
        product = Product.objects.filter(brand = BRANDID, status = 'Publish')
    elif ATOZID:
        product = Product.objects.filter(status = 'Publish').order_by('name')
    elif ZTOAID:
        product = Product.objects.filter(status = 'Publish').order_by('-name')
    elif PRICE_LOWTOHIGHID:
        product = Product.objects.filter(status = 'Publish').order_by('price')
    elif PRICE_HIGHTOLOWID:
        product = Product.objects.filter(status = 'Publish').order_by('-price')
    elif NEW_PRODUCTID:
        product = Product.objects.filter(status = 'Publish', condition = 'New').order_by('-id')
    elif OLD_PRODUCTID:
        product = Product.objects.filter(status = 'Publish', condition = 'Old').order_by('-id')
    else:
        product = Product.objects.filter(status = 'Publish').order_by('-id')


    context = {
        'product': product,
        'categories': categories,
        'filter_price': filter_price,
        'color': color,
        'brand': brand,
    }

    return render(request, 'main/product.html',context)


def SEARCH(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains = query)
    
    context = {
        'product': product
    }
    return render(request, 'main/search.html', context)