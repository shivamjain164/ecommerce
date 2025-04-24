from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("<int:page_num>", views.index , name="index"),
    path("", views.index),
    path("product/<str:search>/<int:page_num>", views.search, name="search"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name = "checkout"),
    path("order_details/", views.order_details, name = "order_details"),
    path("login/", auth_views.LoginView.as_view(template_name = "product/login.html"), name = "login"),
    path("logout/", views.user_logout , name = "logout"),
    path("register/", views.register, name = "register"),
    path("address/", views.address, name = "address"),
    path("profile", views.profile, name = "profile"),
]