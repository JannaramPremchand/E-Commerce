
from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from Products.models import Product_item
from Products.models import ColorVariant
from Products.models import SizeVariant

class Profile(BaseModel):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100 , null=True , blank=True)
    profile_image = models.ImageField(upload_to = 'profile')


    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid =False ,cart__user = self.user).count()

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    is_paid = models.BooleanField(default=False)

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        total = 0
        for cart_item in cart_items:
            total += cart_item.get_total_price()
        return total


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product_item, on_delete=models.CASCADE, blank=True)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.CASCADE, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)  # Assuming you have a quantity field

    def get_total_price(self):
        price = self.product.price
        if self.color_variant:
            price += self.color_variant.price
        if self.size_variant:
            price += self.size_variant.price
        return price * self.quantity


"""class Cart(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='carts')
    is_paid = models.BooleanField(default=False)

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price=[]
        for cart_item in cart_items:
            price.append(cart_item.product.price)
            if cart_item.color_variant:
                color_variant_price = cart_item.color_variant_price.price
                price.append(color_variant_price)
            if cart_item.size_variant:
                size_variant_price = cart_item.size_variant_price.price
                price.append(size_variant_price)
        
        return sum(price)


class CartItems(BaseModel):
    cart =models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    product = models.ForeignKey(Product_item,on_delete=models.CASCADE,blank=True)
    color_variant = models.ForeignKey(ColorVariant ,on_delete=models.CASCADE,null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant,on_delete=models.CASCADE,null=True ,blank=True)

    def get_product_price(self):
            price=[self.product.price]

            if self.color_variant:
                color_variant_price = self.color_variant.price
                price.append(color_variant_price)
            if self.size_variant:
                size_variant_price = self.size_variant.price
                price.append(size_variant_price) 
            return sum(price)
"""
@receiver(post_save , sender = User)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance , email_token = email_token)
            email = instance.email
            send_account_activation_email(email , email_token)

    except Exception as e:
        print(e)

