from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .models import Account
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
def doctorLogin(request):
   # return render(request, 'claim/login.html')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        userId = User
        account = Account.objects.get(user = user)
        print(user)
        print (account)
        print (account.accountType)
        if user is not None and account.accountType == 'Doctor':
            login(request, user)
            return HttpResponseRedirect(reverse("claim:doctor"))
        else:
            return render(request, "claim/login.html")
    return render(request, "claim/login.html")

def claimsLogin(request):
    #return render(request, 'claim/login.html')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        account = Account.objects.get(user = user)
        if user is not None and account.accountType == 'Claims':
            login(request, user)
            return HttpResponseRedirect(reverse("claim:claims"))
        else:
            return render(request, "claim/login.html")
    return render(request, "claim/login.html")

def logoutView(request):
    logout(request)
    return render(request, "claim/login.html", {
        "message": "Logged out."
    })


def doctorHome(request):
    user = request.user
    account = Account.objects.get(user = user)
    if account.accountType == 'Doctor':
        return render(request, "claim/doctorHome.html")
    return render(request, "claim/login.html")

def claimsHome(request):
    user = request.user
    account = Account.objects.get(user = user)
    if account.accountType == 'Claims':
        return render(request, "claim/claimsHome.html")
    return render(request, "claim/login.html")
    