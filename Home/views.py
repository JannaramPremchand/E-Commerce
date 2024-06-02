from django.shortcuts import render
from Products.models import Product_item



def index(request):

    context = {'products':Product_item.objects.all()}
    return render(request,'home/index.html',context)