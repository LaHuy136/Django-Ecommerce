# type: ignore
from django.shortcuts import render, redirect
from E_Shop.models import Product, Categoires, Filter_Price, Color, Brand, Contact_us, Order
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from cart.cart import Cart

import paypalrestsdk
from django.urls import reverse

import uuid
import datetime

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

def PRODUCT_DETAIL_PAGE(request, id):
    prod = Product.objects.filter(id = id).first()

    context = {
        'prod': prod,
    }
    return render(request, 'Main/product_single.html', context)

def Contact_Page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        subject = subject
        message = message
        email_form = settings.EMAIL_HOST_USER
        try:
            send_mail(subject,message,email_form, ['rimpvd76@gmail.com'])
            contact.save()
            return redirect('home')
        except:
            return redirect('contact')

    return render(request, 'Main/contact.html')

def HandleRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        customer = User.objects.create_user(username, email, pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('home')

    return render(request, 'Registration/auth.html')

def HandleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    return render(request, 'Registration/auth.html')


def HandleLogout(request):
    logout(request)
    return redirect('home')

def CART(request):
    return render(request, 'Cart/cart_details.html')

@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'Cart/cart_details.html')


#payment
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

def Check_out(request):
    return render(request, 'Cart/checkout.html')

def PLACE_ORDER(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        # print(user)
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = int(request.POST.get('postcode'))
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        # print(firstname, lastname, country, address, city, postcode, phone, email)

        
        cart_items = []
        cart_total_amount = 0

        if 'cart' in request.session:
            for key, value in request.session['cart'].items():
                # Chuyển đổi value['price'] và value['quantity'] sang kiểu int
                item_price = int(value['price'])
                item_quantity = int(value['quantity'])

                cart_item = {
                    'name': value['name'],  
                    'quantity': item_quantity, 
                    'price': item_price,  
                    'total_price': item_price * item_quantity  
                }
                cart_items.append(cart_item)

                total_item_price = item_price * item_quantity
                cart_total_amount += total_item_price

        print(cart_items)
        print(cart_total_amount)

        order = Order(
            user = user,
            firstname = firstname,
            lastname = lastname,
            country = country,
            address = address,
            additional_info = "no additional information",
            city = city,
            state = state,
            postcode = postcode,
            phone = phone,
            email = email,
            payment_id = "ORDER_" + str(uuid.uuid4().hex)[:10] + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        order.save()

        

    return render(request, 'Cart/placeorder.html')


def create_payment(request):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('payment_failed')),
        },
        "transactions": [
            {
                "amount": {
                    "total": "10.00",  # Total amount in USD
                    "currency": "USD",
                },
                "description": "Payment for Product/Service",
            }
        ],
    })

    if payment.create():
        return redirect(payment.links[1].href)  # Redirect to PayPal for payment
    else:
        return render(request, 'payment_failed.html')
    

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'payment_success.html')
    else:
        return render(request, 'payment_failed.html')

