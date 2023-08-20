from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from decimal import Decimal
# Create your models here.

class CustomUser(AbstractUser):
#     store_manager = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=300,null=True)
    contact = models.CharField(max_length=20,null=True)
        
# class UserProfile(models.Model):
#         user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#         email = models.EmailField()
#         address = models.CharField(max_length=300)
#         contact = models.CharField(max_length=20)
        
# class Sections(models.Model):
#         name = models.CharField(max_length=100,null=True)
#         create_date = models.DateTimeField(auto_now_add=True,null=True)
#         update_date = models.DateTimeField(blank=True, null=True)
#         delete_sign = models.BooleanField(default=False)
#         delete_date = models.DateTimeField(blank=True, null=True)
#         image = models.ImageField(upload_to='Pictures/',null=True)

class Sections_a(models.Model):
        name = models.CharField(max_length=100,null=True)
        create_date = models.DateTimeField(auto_now_add=True,null=True)
        update_date = models.DateTimeField(blank=True, null=True)
        delete_sign = models.BooleanField(default=False)
        delete_date = models.DateTimeField(blank=True, null=True)
        image = models.ImageField(upload_to='Pictures/',null=True)
        
class Products(models.Model):
        name = models.CharField(max_length=100)
        section = models.ForeignKey(Sections_a,on_delete=models.CASCADE)
        manufacture_date = models.DateField(blank=True,null=True)
        expiring_date = models.DateField(blank=True,null=True)
        rate_per_unit = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
        image = models.ImageField(upload_to='Products/Picture/',null=True)                
        create_date = models.DateTimeField(auto_now_add=True,null=True)
        update_date = models.DateTimeField(blank=True, null=True)
        delete_sign = models.BooleanField(default=False)
        delete_date = models.DateTimeField(blank=True, null=True)     
        quantity = models.IntegerField(blank=True,null=True)   
class UserProducts(models.Model):
            user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
            product = models.ForeignKey(Products,on_delete=models.CASCADE)
            quantity = models.PositiveIntegerField(default=0)
