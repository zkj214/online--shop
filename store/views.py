from django.shortcuts import render
from store.models import *
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.


def store(request):
    if request.user.is_authenticated:
        customer,created=Customer.objects.get_or_create(user=request.user)
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.cartitem_set.all() #one to many relationship
        cartitems=order.get_cart_items
    else:
        items=[]
        order={"get_cart_items":0,"get_cart_total":0,"shipping":False}
        cartitems=order["get_cart_items"]

    products=Product.objects.all()
    p=Paginator(products,3)
    page=request.GET.get("page")
    products=p.get_page(page)
    nums='a'* products.paginator.num_pages

    context={"products":products,"cartitems":cartitems,"nums":nums}
    return render(request,"store/store.html",context)


def search_items(request):
    if request.user.is_authenticated:
        customer,created=Customer.objects.get_or_create(user=request.user)
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.cartitem_set.all() #one to many relationship
        cartitems=order.get_cart_items
    else:
        items=[]
        order={"get_cart_items":0,"get_cart_total":0,"shipping":False}
        cartitems=order["get_cart_items"]

    keyword=request.POST.get("search")
    products=Product.objects.filter(name__icontains=keyword)
    count=products.count()

    p = Paginator(products, 3)
    page = request.GET.get("page")
    products = p.get_page(page)
    nums = 'a' * products.paginator.num_pages

    context={"products":products,"nums":nums,"count":count,"keyword":keyword,"cartitems":cartitems}
    return render(request,"store/search_items.html",context)


@login_required
def cart(request):
    if request.user.is_authenticated:
        customer,created=Customer.objects.get_or_create(user=request.user)
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.cartitem_set.all() #one to many relationship
        cartitems = order.get_cart_items

    else:
        items=[]
        order={"get_cart_items":0,"get_cart_total":0,"shipping":False}
        cartitems=order["get_cart_items"]


    context={"items":items,"order":order,"cartitems":cartitems}
    return render(request,"store/cart.html",context)


@login_required
def checkout(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.cartitem_set.all()  # retrieving items from one to many relationship
        cartitems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0,"shipping":False}
        cartitems=order["get_cart_items"]

    context = {"items": items, "order": order,"cartitems":cartitems}
    return render(request,"store/checkout.html",context)


def product_info(request,pk):
    product=Product.objects.get(pk=pk)

    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.cartitem_set.all()  # retrieving items from one to many relationship
        cartitems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartitems=order["get_cart_items"]

    context={"product":product,"cartitems":cartitems}
    return render(request,"store/product_detail.html",context)

#class ProductDetail(DetailView):
#    model=Product

#    def get_queryset(self,*args,**kwargs):
#        queryset=super().get_queryset(*args,**kwargs)
#         return queryset.filter(pk=self.kwargs.get("pk"))


@login_required
def UpdateCart(request):
    data=json.loads(request.body) #reading the json object
    productID=data["productID"]
    action = data["action"]
    print(f"Product: {productID}")
    print(f"Action: {action}")

    customer,created=Customer.objects.get_or_create(user=request.user)
    product=Product.objects.get(pk=productID)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    cartitem,created=CartItem.objects.get_or_create(product=product,order=order)

    if action=="add":
        cartitem.quantity+=1
    elif action=="remove":
        cartitem.quantity-=1

    cartitem.save()

    if cartitem.quantity==0:
        cartitem.delete()

    return JsonResponse("Item was added",safe=False) # we send data from javascript to python using json


@login_required
def ProcessOrder(request):
    transaction_id=datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer,created=Customer.objects.get_or_create(user=request.user)
        order,created=Order.objects.get_or_create(customer=customer,complete=False)

        total=float(data["user"]["total"])  # converts string data to float data cuz it's a dictionary
        order.transaction_id=transaction_id #updates the transaction_id field of order model

        if total == float(order.get_cart_total): #float is not the same as decimal. that's why we converted the cart total to float
            order.complete=True
            cartitems=order.cartitem_set.all()

            for item in cartitems:
                pk=item.product.pk
                product=Product.objects.get(pk=pk)
                product.sales+=1
                product.stocks-=1
                product.save()

        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data["shipping"]["address"],
                city=data["shipping"]["city"],
                state=data["shipping"]["state"],
                zipcode=data["shipping"]["zipcode"]
            )
    else:
        print("User is not logged in.")

    return JsonResponse("Payment submitted...",safe=False) # we send data from javascript to python using json