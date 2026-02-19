from django.db import models
from django.utils import timezone

class CustomerData(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=128)

class Cart(models.Model):
    user = models.ForeignKey(CustomerData, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='product_photos/') 
    def __str__(self): 
        return f"{self.name} | ₹{self.price} | {self.description}"


class Order(models.Model):
    user  = models.ForeignKey(CustomerData, on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    quantity = models.IntegerField()
    subtotal = models.FloatField(default=0) 
    image = models.ImageField(upload_to='product_photos/', null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True,null=True)    