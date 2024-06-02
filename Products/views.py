from django.shortcuts import render
from Products.models import Product_item
from Account.models import CartItems
from django.http import HttpResponseRedirect



"""def get_product(request , slug):
    try:
        product = Product_item.objects.get(slug =slug)
        return render(request  , 'product/product.html' , context = {'product' : product})

    except Exception as e:
        print(e)"""
def get_product(request,slug):
    print("*************")
    print(request.user)
    print("*************")
    print(request.user.profile.get_cart_count)
    try:
        product = Product_item.objects.get(slug =slug)
        context ={'product':product}
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price
            print(price)
        
        return render(request,'product/product.html', context=context)

    except Exception as e:
        print(e)



def remove_cart(request,cart_item_uid):
    cart_item = CartItems.objects.get(uid = cart_item_uid)
    cart_item.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



