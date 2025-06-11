from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    digital=models.BooleanField(default=False,null=True,blank=True)
    image=models.ImageField(blank=True,null=True,upload_to="uploaded_pics")
    description=models.TextField(default='')
    stocks=models.IntegerField(default=10,null=True,blank=True)
    sales=models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return self.name

    @property
    def ImageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url
    

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered=models.DateTimeField(auto_now=True,blank=True,null=True)
    complete=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.pk)
    
    @property
    def get_cart_total(self):
        orderitems=self.cartitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems=self.cartitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping=False
        cartitems=self.cartitem_set.all()

        for item in cartitems:
            if not item.product.digital:
                shipping=True
        return shipping


class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.IntegerField(default=0,blank=True,null=True)
    date_added=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.date_added)

    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address=models.CharField(max_length=100,blank=True,null=True)
    city=models.CharField(null=True)
    state=models.CharField(null=True)
    zipcode=models.IntegerField(blank=True,null=True)
    date_added=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address

