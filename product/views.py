from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Count
from . import models
from . import forms
# Create your views here.


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
        return render(request, "product/index.html", {
            "product_list": product,
            "form": forms.Searchform(), 
            "form1":forms.Cartform(),
            "cart_list": models.Cart_added.objects.all(),
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
            "cart_list": models.Cart_added.objects.all(),
            })
    else:
        return HttpResponse("No results found")

# Code for landing page finishes here

# Code for cart 
def cart(request):
    # Get the post from inex to cart and get ID in the form
    if request.method == "POST":
        cart_form = forms.Cartform(request.POST)

        if cart_form.is_valid():
            product_name = cart_form.cleaned_data["product"]

            product = models.Product.objects.get(id=product_name)
            product_in_cart = models.Cart_added.objects.filter(product = product)
            if product_in_cart:
                product_in_cart = models.Cart_added.objects.get(product=product)
                product_in_cart.quantity = product_in_cart.quantity + 1
                product_in_cart.save()
                
            else:
                # If the added product is not in cart, the new row is created in cart table
                cart_item = models.Cart_added(product=product)
                cart_item.save()
            
            # return render(request, "product/cart.html")
    cart_list = models.Cart_added.objects.all()
    
    return render(request, "product/cart.html",{
        "cart_list":cart_list
    })
    
    
# Code for cart finishes here
    # Cde for checkout page
# Code for checkout page
def checkout(request):
    # Get the cart data to checkout page
    cart_data = models.Cart_added.objects.all()
    total = 0
    for i in cart_data:
        i.product.price = i.product.price * i.quantity
        total += i.product.price 
    checkout_form = forms.Checkoutform()
    
    if request.method == "POST":
        checkout_form = forms.Checkoutform(request.POST)
        # total = 0
        if checkout_form.is_valid():
            #  Get cart details
            cart_data = models.Cart_added.objects.all()
            id_cart = cart_data[0].id
       
            # Save the data to the database
            order = models.OrderPlaced()
         
            
            for i in cart_data:
                order = models.OrderPlaced()
                order.product = i.product
                order.cart_id = id_cart
                order.quantity = i.quantity
                order.name = checkout_form.cleaned_data["name"]
                order.email = checkout_form.cleaned_data["email"]
                order.address = checkout_form.cleaned_data["address"]
                order.city = checkout_form.cleaned_data["city"]
                order.state = checkout_form.cleaned_data["state"]
                order.zip_code = checkout_form.cleaned_data["zip_code"]
                order.total = i.product.price * i.quantity
                order.save()
            
            # Clear the cart after checkout
            models.Cart_added.objects.all().delete()
            return render(request,"product/order_placed.html", {
                "cart_list":models.Cart_added.objects.all(),
                
            })
    
    
    return render(request, "product/checkout.html", {
        "checkout_form":checkout_form,
        "cart_data":cart_data,
        "total":total,
        "cart_list": models.Cart_added.objects.all(),
    })