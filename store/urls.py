from django.urls import path
from store.views import *
from accounts import views

app_name="store"
urlpatterns = [
    path("",views.login_user,name="index"),
    path("store/",store,name="items"),
    path("cart/",cart,name="cart"),
    path("checkout/",checkout,name="checkout"),
    path("product_info/<int:pk>",product_info,name="product_info"),
    path("update_cart/",UpdateCart,name="update_cart"),
    path("process_order/",ProcessOrder,name="process_order"),
    path("search_items/",search_items,name="search")
]