from django.urls import path
from Account.views import *
from Products.views import *

urlpatterns = [
    path('login/',login_page,name='login'),
    path('register/',register_page,name='register'),
    path('activate/<email_token>/',activate_email,name='email'),
    path('cart/',cart,name='cart'),
    path('add-to-cart/<uid>/',add_to_cart,name='add_to_cart'),
    path('remove_cart/<cart_item_uid>/',remove_cart,name='remove_cart')
]