from django.shortcuts import render,redirect
from accounts.forms import  CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def login_user(request):
    if request.user.is_authenticated:
        return  redirect("store:items")
    else:
        if request.method=="POST":
            username=request.POST.get("username")
            password=request.POST.get("password")

            user=authenticate(username=username,password=password)

            if user is not None:
                login(request,user)
                messages.success(request,"You have successfully logged in.")
                return redirect("store:items")
            else:
                messages.info(request,"Wrong username or password.")
                return redirect("accounts:login")

        context={}
    return render(request,"accounts/login.html",context)


def register_user(request):
    if request.user.is_authenticated:
        return redirect("store:items")
    else:
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)

            if form.is_valid:
                form.save()
                messages.success(request, "Your account has been successfully created. You can now login.")
                return redirect("accounts:login")
            else:
                messages.warning(request, "There was an error encountered. Pls try again.")
                return redirect("accounts:register")
        context={"form":form}
    return render(request,"accounts/register.html",context)


def logout_user(request):
    logout(request)
    messages.success(request,"You have been successfully logged out.")
    return redirect("accounts:login")