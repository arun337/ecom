from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.http.response import JsonResponse
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    featured_product=Product.objects.filter(trending=1)
   
   
   
    context={
        'featured_product':featured_product,
        
    
        
    }
    return render(request,'home/index.html',context)


def category(request):
    category=Category.objects.filter(status=0)
    context={'category':category}
    return render(request,'category/category.html',context)


def collection(request,slug):
    if(Category.objects.filter(slug=slug,status=0)):
       products=Product.objects.filter(category__slug=slug)
       category=Category.objects.filter(slug=slug).first()
       context={
                'products':products,
                'category':category
                
                }
       return render(request,"product/index.html",context)
    else:
        messages.warning(request,"No such category")
        return redirect('category')#'category:name of url'
   
def productdetail(request,cate_slug,prod_slug):
    if(Category.objects.filter(slug=cate_slug,status=0)):
        if(Product.objects.filter(slug=prod_slug,status=0)):
           products=Product.objects.filter(slug=prod_slug,status=0).first
           context={
               'products':products

           }
        else:
            messages.error(request,"No such Products")
            return redirect('category')
    else:
        messages.error(request,"No such Categories")
        return redirect('category')
    return render(request,'product/products_description.html',context)


def addtocart(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            prod_id=int(request.POST.get('product_id'))
            product_check=Product.objects.get(id=prod_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user.id,product_id=prod_id)):
                    return JsonResponse({'status':"Product Already in Cart" })
                else:
                    prod_qty=int(request.POST.get('product_qty'))

                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user,product_id=prod_id,product_qty=prod_qty)
                        return JsonResponse({'status':"Product added Succesfully"})
                    else:
                        return JsonResponse({'status':"Only" + str(product_check.quantity) + "quantity available"})


            else:
                return JsonResponse({'status':"No such Product Found"})
        else:
            
            return JsonResponse({'status':"Login to Continue"})
            
    return redirect('category')

@login_required(login_url="account")
def cart(request):
    cart=Cart.objects.filter(user=request.user)
    context={
        'cart':cart
    }
    return render(request,'cart/cart.html',context)


def updatecart(request):
    if request.method =='POST':
        prod_id=int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user,product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id,user=request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status':"Update Successfully"})
    return redirect('index')

def deletecartitem(request):
    if request.method =='POST':
        prod_id=int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user,product_id=prod_id)):
            cartitem=Cart.objects.get(product_id=prod_id, user=request.user)
            cartitem.delete()
            return JsonResponse({'status':"Deleted Successfully"})
    return redirect('index')


@login_required(login_url="account")
def wishlist(request):
    wishlist=Whishlist.objects.filter(user=request.user)
    context={
        'wishlist':wishlist
    }
    return render(request,'cart/wishlist.html',context)

def viewwish(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            prod_id=int(request.POST.get('product_id'))
            product_check=Product.objects.get(id=prod_id)
            if(product_check):
                if(Whishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status':"Product already in wishlist"})
                else:
                    Whishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status':"Product added to wishlist"})
            else:
                return JsonResponse({'status':"No such product"})

        else:
            return JsonResponse({'status':"Login to continue"})

    return redirect('index')


def deleteitem(request):
    if request.method=='POST':
        if request.user.is_authenticated:
              prod_id=int(request.POST.get('product_id'))
              if(Whishlist.objects.filter(user=request.user, product_id=prod_id)):
                    wishlistitem=Whishlist.objects.get(product_id=prod_id)
                    wishlistitem.delete()
                    return JsonResponse({'status':"Product removed from wishlist"})
              else:
                    Whishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status':"Product not found in wishlist"})
            
        else:

            return JsonResponse({'status':"Login to continue"})

    return redirect('index')

def checkout(request):
    rawcart=Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id)
    cartitem=Cart.objects.filter(user=request.user)
    total_price=0
    for item in cartitem:
        total_price=total_price + item.product.selling_price * item.product_qty
    userprofile=Profile.objects.filter(user=request.user.id).first()
    context={
        'cartitem':cartitem,
        'total_price':total_price,
        'userprofile':userprofile
    }
    return render(request,"cart/checkout.html",context)

import random

@login_required(login_url="account")
def placeorder(request):
    if request.method == 'POST':
        print("hello")
        if not Profile.objects.filter(user=request.user):
            userprofile=Profile()
            userprofile.user=request.user
            userprofile.phone=request.POST.get('phone')
            userprofile.address=request.POST.get('address')
            userprofile.city=request.POST.get('city')
            userprofile.state=request.POST.get('state')
            userprofile.country=request.POST.get('country')
            userprofile.pincode=request.POST.get('pincode')
            userprofile.save()


        neworder=Order()
        neworder.user=request.user
        neworder.fname=request.POST.get('fname')
        neworder.lname=request.POST.get('lname')
        neworder.email=request.POST.get('email')
        neworder.phone=request.POST.get('phone')
        neworder.address=request.POST.get('address')
        neworder.city=request.POST.get('city')
        neworder.state=request.POST.get('state')
        neworder.country=request.POST.get('country')
        neworder.pincode=request.POST.get('pincode')
        neworder.payment_mode=request.POST.get('payment_mode')
        neworder.payment_id=request.POST.get('payment_id')
        cart=Cart.objects.filter(user=request.user)
        cart_total_price=0
        for item in cart:
            cart_total_price=cart_total_price + item.product.selling_price * item.product_qty

        neworder.total_price=cart_total_price
        trackno='hello' + str(random.randint(11111,99999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno='hello' + str(random.randint(11111,99999))
        neworder.tracking_no=trackno
        neworder.save()

        neworderitems=Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderedItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )

            orderproduct=Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity=orderproduct.quantity - item.product_qty
            orderproduct.save()

        Cart.objects.filter(user=request.user).delete()
        messages.success(request,"Your order has been placed")

        payMode=request.POST.get('payment_mode')
        if(payMode=="Razor Pay" or payMode=="Pay Pal"):
            return JsonResponse({'status':"Your order has been placed"})


    return redirect('index')

@login_required(login_url="account")
def proccedtopay(request):
    cart=Cart.objects.filter(user=request.user)
    total_price=0
    for item in cart:
        total_price=total_price+item.product.selling_price * item.product_qty
    return JsonResponse({'total_price':total_price})

def myorder(request):
    
    orders=Order.objects.filter(user=request.user)
    ord=OrderedItem.objects.all()
    
    context={
        'orders':orders,
        'ord':ord

    }
    return render(request,'cart/order.html',context)

def vieworder(request,t_no):
    order=Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems=OrderedItem.objects.filter(order=order)
    context={
        'order':order,
        'orderitems':orderitems
    }
    return render(request,'cart/orderview.html',context)


def paymentComplete(request):
	body = json.loads(request.body)
	print('BODY:', body)
	return JsonResponse('Payment completed!', safe=False)