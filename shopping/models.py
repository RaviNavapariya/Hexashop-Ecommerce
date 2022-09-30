from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BuyerProfile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
    # username = models.CharField(max_length=100,blank=True,null=True)
    # firstname = models.CharField(max_length=100,blank=True,null=True)
    # lastname = models.CharField(max_length=100,blank=True,null=True)
    # email = models.EmailField(max_length=100,blank=True,null=True)
    # password1 = models.CharField(max_length=100,blank=True,null=True)
    # password2 = models.CharField(max_length=100,blank=True,null=True)
    mob= models.CharField(max_length=50,blank=True,null=True)
    gender = models.CharField(max_length=50,blank=True,null=True)
    hobby= models.CharField(max_length=50,blank=True,null=True)
    dob = models.DateField()
    
    def __str__(self): 
        return self.user.username

class SellerProfile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
    # username = models.CharField(max_length=100,blank=True,null=True)
    # firstname = models.CharField(max_length=100,blank=True,null=True)
    # lastname = models.CharField(max_length=100,blank=True,null=True)
    # email = models.EmailField(max_length=100,blank=True,null=True)
    # password1 = models.CharField(max_length=100,blank=True,null=True)
    # password2 = models.CharField(max_length=100,blank=True,null=True)
    mob= models.CharField(max_length=50,blank=True,null=True)
    gender = models.CharField(max_length=50,blank=True,null=True)
    hobby= models.CharField(max_length=50,blank=True,null=True)
    dob = models.DateField()    
    
    def __str__(self): 
        return self.user.username



class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    image = models.ImageField(upload_to='mensimages',null=True,blank=True)
    price = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    item_quantity = models.PositiveIntegerField(default=1)
    item_amount = models.IntegerField()

    def __str__(self)->str:
        return self.product.name


class OrderDetail(models.Model):

    id = models.BigAutoField(primary_key=True)
    customer_email = models.EmailField(verbose_name='Customer Email')
    product = models.ForeignKey(Cart, verbose_name='Product', on_delete=models.CASCADE, null=True)
    amount = models.IntegerField(verbose_name='Amount')
    stripe_payment_intent = models.CharField(max_length=200)
    # This field can be changed as status
    has_paid = models.BooleanField(default=False, verbose_name='Payment Status')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)