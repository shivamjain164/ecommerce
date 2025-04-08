from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("<int:page_num>", views.index , name="index"),
    path("", views.index),
    path("product/<str:search>/<int:page_num>", views.search, name="search"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name = "checkout")
]