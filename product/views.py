from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Count
from . import models
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.

# Fnction to create the cart_list for all pages. Showing cat items in the header
def cart_list_items(request):
    if request.user.is_authenticated:        
        cart_list = models.Cart_added.objects.filter(user = request.user)
    else:
        cart_list = models.Cart_added.objects.filter(user = None)

    return cart_list


# Code for landing page
def index(request,page_num=1):
    if request.method == "POST":
        search_form = forms.Searchform(request.POST)
        if search_form.is_valid():
            search = search_form.cleaned_data["search"]
            print("I have reached here")
            return redirect("search", search=search, page_num=1)
    else:
        product_list = models.Product.objects.all().order_by("name")
        p = Paginator(product_list, 4)  # Show 4 products per page
        page = page_num
        # product = p.page(page)
        if page is None:
            product = p.page(1)
        elif page > p.num_pages:
            product = p.page(p.num_pages)
        else:
            product = p.page(page)
        # print(request.user)
       
        return render(request, "product/index.html", {
            "product_list": product,
            "form": forms.Searchform(), 
            "form1":forms.Cartform(),
            "cart_list": cart_list_items(request),
            })

def search(request, search, page_num):
    product_list = models.Product.objects.filter(name__icontains=search).order_by("name")
    # print(product_list)
    if product_list:
        p = Paginator(product_list, 4)  # Show 4 products per page
        page = page_num
            # product = p.page(page)
        if page is None:
            product = p.page(1)
        elif page > p.num_pages:
            product = p.page(p.num_pages)
        else:
            product = p.page(page)
        
        return render(request, "product/index.html", {
            "product_list": product,
            "form": forms.Searchform(),
            "form1":forms.Cartform(),
            "cart_list": cart_list_items(request),
            })
    else:
        return HttpResponse("No results found")

# Code for landing page finishes here

# Code for cart 
def cart(request):
    # Get the post from inex to cart and get ID in the form
    if request.method == "POST":
        cart_form = forms.Cartform(request.POST)
        user = request.user
        # print(user)
        if cart_form.is_valid():
            product_name = cart_form.cleaned_data["product"]
            
            product = models.Product.objects.get(id=product_name)
            if user.is_authenticated:
                product_in_cart = models.Cart_added.objects.filter(product = product, user = user)
            else:
                product_in_cart = models.Cart_added.objects.filter(product = product, user = None)
            if product_in_cart:
                # product_in_cart = models.Cart_added.objects.f(product=product)
                for product in product_in_cart:
                    # print(product.product.name)
                    # print(product.quantity)
                    product.quantity = product.quantity + 1
                    product.save()
                
            else:
                # If the added product is not in cart, the new row is created in cart table
                if user.is_authenticated:
                    cart_item = models.Cart_added(product=product, user = user)
                    cart_item.save()
                else:
                    cart_item = models.Cart_added(product=product, user = None)
                    cart_item.save()
            
            # return render(request, "product/cart.html")
    # if user is not None:        
    #     cart_list = cart_list_items(request)
    # else:
    #     cart_list = cart_list_items(None)
        return redirect("index", page_num=1)
    else:
        return render(request, "product/cart.html",{
            "cart_list":cart_list_items(request),
        })
    
    
# Code for cart finishes here
    # Cde for checkout page
# Code for checkout page
def checkout(request):
    # Get the cart data to checkout page
    existing_address = None
    if request.user.is_authenticated:
        cart_data = models.Cart_added.objects.filter(user = request.user)
        existing_address = models.Address.objects.filter(user = request.user, default = True)
    else:
        cart_data = models.Cart_added.objects.filter(user = None)
    total = 0
    for i in cart_data:
        i.product.price = i.product.price * i.quantity
        total += i.product.price 
    checkout_form = forms.Checkoutform()
    
    
    
    if request.method == "POST":
        checkout_form = forms.Checkoutform(request.POST)
        if checkout_form.is_valid():
            #  Get cart details
            if request.user.is_authenticated:
                cart_data = models.Cart_added.objects.filter(user = request.user)
                existing_address = models.Address.objects.filter(user = request.user, default = True)
                address_user = request.user
            else:
                cart_data = models.Cart_added.objects.filter(user = None)
            id_cart = cart_data[0].id
            # Save the address details in the address table
            
            
            if existing_address:
                default = False
              
            else:
                default = True
                address = models.Address()
                if request.user.is_authenticated:
                    address_user = request.user
                else:
                    existing_user = models.User.objects.filter(username = checkout_form.cleaned_data["email"])
                    if existing_user:
                        address_user = existing_user[0]
                    else:
                    # address.user = None
                    # To be coded. Create a new user with default password and email as username
                        user  = models.User.objects.create_user(
                            username = checkout_form.cleaned_data["email"],
                            email = checkout_form.cleaned_data["email"],
                            password = checkout_form.cleaned_data["name"]
                        )
                        
                        user.save()
                        address_user = models.User.objects.get(username = checkout_form.cleaned_data["email"])
                # address.user = request.user
                if models.Address.objects.filter(user = address_user, default = True):
                    print("Address already exists")
                else:
                    address = models.Address()
                    address.user = address_user
                    address.name = checkout_form.cleaned_data["name"]
                    address.email = checkout_form.cleaned_data["email"]   
                    address.address = checkout_form.cleaned_data["address"]   
                    address.city = checkout_form.cleaned_data["city"]
                    address.state = checkout_form.cleaned_data["state"]
                    address.zip_code = checkout_form.cleaned_data["zip_code"]
                    address.default = default
                    
                    address.save()
                    
                    
            
            
            # Save the data to the database
            order = models.OrderPlaced()
            cart_data = models.Cart_added.objects.filter(user = address_user)    
            for i in cart_data:
                order = models.OrderPlaced()
                order.address = models.Address.objects.get(user = address_user, default = True)
                # print(address)
                order.product = i.product
                order.cart_id = id_cart
                order.quantity = i.quantity
                order.total = i.product.price * i.quantity
                order.user = address_user
                order.save()
            
            # Clear the cart after checkout
            cart_data.delete()
            login(request, address_user)
            return redirect("order_details")
    
    if existing_address:
        prefill_address = existing_address[0]
        return render(request, "product/checkout.html", {
        "checkout_form":checkout_form,
        "cart_data":cart_data,
        "total":total,
        "cart_list": cart_list_items(request),
        "existing_address":prefill_address,
    })
    else:
    
        return render(request, "product/checkout.html", {
            "checkout_form":checkout_form,
            "cart_data":cart_data,
            "total":total,
            "cart_list": cart_list_items(request),
            
        })
    
    
    # Check the order details in a page for all the orders placed
def order_details(request):
    # Get the order details from the order placed table
    order_data = []
    cart = models.OrderPlaced.objects.order_by().values("cart_id").distinct() 
    print(cart)
    for i in range(0,len(cart)):
        order_id=cart[i]["cart_id"]
        if request.user.is_authenticated:
            order_value = models.OrderPlaced.objects.filter(cart_id=order_id, user = request.user)
            if order_value:
                order_data.append(order_value)
        else:
            order_data.append(models.OrderPlaced.objects.filter(cart_id=order_id, user = None))    
    # for order in order_data:
    #     for i in range(0,len(order)):
    #         print(order[i])
    print(order_data)
    return render(request, "product/order_details.html", {
        "order_data":order_data,
        "cart_list": cart_list_items(request),
    })
  
  
@login_required    
def user_logout(request):
    logout(request)
    return redirect("index", page_num=1)

def register(request):
    if request.method == "POST":
        form = forms.Registrationform(request.POST)
        # print(form)
        if form.is_valid():
            user = models.User.objects.filter(email = form.cleaned_data["email"])
            if user.exists():
                messages.error(request, "Email already exists")
                return redirect("register")
            
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            email = form.cleaned_data.get("email")
            user = authenticate(username=username, password=password, email = email)
            login(request, user)
            return redirect("index", page_num=1)
        else:
            messages.error(request, "Invalid form submission")
            return redirect("register")
    else:
        form = forms.Registrationform()
    return render(request, "product/register.html", {
        "form":form,
        "cart_list": cart_list_items(request),
    })
    
    
def address(request):
    return HttpResponse("Address page")

@login_required
def profile(request):
    if request.method == "POST":
        user_form = forms.Checkoutform(request.POST)
        print(user_form)
        if user_form.is_valid():
            print("Reached valid form")
            address_list = models.Address.objects.filter(user = request.user, default = True)
            if address_list:
                address = address_list[0]
            else:
                address = models.Address()
            address.user = request.user
            address.name = user_form.cleaned_data["name"]
            address.email = user_form.cleaned_data["email"]
            address.address = user_form.cleaned_data["address"]
            address.city = user_form.cleaned_data["city"]
            address.state = user_form.cleaned_data["state"]
            address.zip_code = user_form.cleaned_data["zip_code"]
            address.default = True
            print(address.email)
            address.save()
        else:
            print("Form is not valid")
            
        return redirect("profile")
    else:    
        print("Post is not triggered")
        user_info = models.Address.objects.get(user = request.user)
        
        if user_info:
            user_form = forms.Checkoutform(initial={
            "name":user_info.name,
            "email":user_info.email,
            "address":user_info.address,
            "city":user_info.city,
            "state":user_info.state,
            "zip_code":user_info.zip_code,
            })
            return render(request, "product/profile.html", {
                "user_info":user_form,
                "cart_list": cart_list_items(request),
            })
        else:
            return render(request, "product/profile.html", {
                "cart_list": cart_list_items(request),
            })