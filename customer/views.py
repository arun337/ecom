from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Customer
from django.contrib import messages
# Create your views here.

def signout(request):
    logout(request)
    success_message="Logged Out Successfully"
    messages.success(request,success_message)
    return redirect('index')

def show_account(request):
    user=None
    context={}
    if request.POST and 'register' in request.POST:
        context['register']=True
        try:
            username=request.POST.get('username')
            password=request.POST.get('password')
            email=request.POST.get('email')
            address=request.POST.get('address')
            phone=request.POST.get('phone')
            
        
        #create user account
            user=User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
        #create customer account
            customer=Customer.objects.create(
                name=username,
                user=user,
                phone=phone,
                address=address
            )
            success_message="User Registered Sucessfully"
            messages.success(request,success_message)
        except Exception as e:
            error_message="Duplicate username"
            messages.error(request,error_message)
    if request.user.is_authenticated:
        
        return redirect('index')
    else:
        if request.POST and 'login' in request.POST:
            context['register']=False
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                success_message="Logged in Successfully"
                messages.success(request,success_message)
                return redirect('index')
            else:
                messages.error(request,'Invalid Input')
        return render(request,'account/account_layout.html',context)