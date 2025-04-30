from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.Allorders.as_view(), name='allorders'),      
    path('orders/<str:username>/', views.OrderByUser.as_view(), name='order_by_user'), 
]
