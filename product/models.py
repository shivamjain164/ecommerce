from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    image = models.FileField(upload_to='images/')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return self.name
    
    
class Cart_added(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    




    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    default = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    
class OrderPlaced(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    # name = models.CharField(max_length=100)
    # email = models.EmailField()
    # address = models.TextField()
    # city = models.CharField(max_length=100)
    # state = models.CharField(max_length=100)
    # zip_code = models.CharField(max_length=10)
    total = models.IntegerField()
    quantity = models.IntegerField(default=1)
    cart_id = models.CharField(max_length=100, default="1")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   
    
    def __str__(self):
        return self.cart_id
    
    