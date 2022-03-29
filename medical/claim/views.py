from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .models import Account, Claim
from django.contrib.auth.mixins import LoginRequiredMixin
import joblib

svm_job = joblib.load('ml/svm.pkl')
knn_job = joblib.load('ml/knn.pkl')
logistic_job = joblib.load('ml/logistics.pkl')
gauss_job = joblib.load('ml/gauss.pkl')
trees_job = joblib.load('ml/extraTrees.pkl')
forest_job = joblib.load('ml/randForest.pkl')





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
        if request.method == "POST":
            claim = request.POST["claim"]
            tariff = request.POST["tariff"]
            age = request.POST["age"]
            practice = request.POST["practice"]
            gender = request.POST["gender"]
            if gender == "M":
                genderNo = 0
            else:
                genderNo = 1
            description = request.POST["description"]
            if description == "PAEDIATRICIANS":
                descriptionNo = 0
            else:
                descriptionNo = 1

            svm_pred = svm_job.predict([[age, genderNo, claim, practice, descriptionNo, tariff]])[0]
            knn_pred = knn_job.predict([[age, genderNo, claim, practice, descriptionNo, tariff]])[0]
            logistic_pred = logistic_job.predict([[age, genderNo, claim, practice, descriptionNo, tariff]])[0]
            gauss_pred = gauss_job.predict([[age, genderNo, claim, practice, descriptionNo, tariff]])[0]
            svm_pred = svm_job.predict([[age, genderNo, claim, practice, descriptionNo, tariff]])[0]
            trees_pred = trees_job.predict([[age, genderNo, claim, practice, descriptionNo, tariff]])[0]
            forest_pred = forest_job.predict([[age, genderNo, claim, practice, descriptionNo, tariff]])[0]
            if knn_pred == 0:
                knn_pred = "Proceed"
            else:
                knn_pred = "Possible Fraud"
            if svm_pred == 1:
                svm_pred = "Proceed"
            else:
                svm_pred = "Possible Fraud"
            if logistic_pred == 1:
                logistic_pred = "Proceed"
            else:
                logistic_pred = "Possible Fraud"
            if gauss_pred == 1:
                gauss_pred = "Proceed"
            else:
                gauss_pred = "Possible Fraud"
            if trees_pred == 1:
                trees_pred = "Proceed"
            else:
                trees_pred = "Possible Fraud"
            if forest_pred == 1:
                forest_pred = "Proceed"
            else:
                forest_pred = "Possible Fraud"


            newClaim = Claim.objects.create(doctor=account, claimed=claim, age=age, gender=gender, practice=practice, description=description, tariff=tariff, approval="Pending", knn=knn_pred, svm=svm_pred, logistics=logistic_pred, bayes=gauss_pred, forest=forest_pred, trees=trees_pred)
            newClaim.save()
            return HttpResponseRedirect(reverse("claim:myclaims"))
        return render(request, "claim/doctorHome.html")
    return render(request, "claim/login.html")

def myClaims(request):
    user = request.user
    account = Account.objects.get(user = user)
    if account.accountType == 'Doctor':
        claims = Claim.objects.filter(doctor = account)
        return render(request, "claim/myClaims.html", {'claims':claims})
    return render(request, "claim/login.html")

def claimsHome(request):
    user = request.user
    account = Account.objects.get(user = user)
    if account.accountType == 'Claims':
        claims = Claim.objects.all()
        return render(request, "claim/allClaims.html", {'claims':claims})
    return render(request, "claim/login.html")

def claimDetail(request, claim_id):
    user = request.user
    account = Account.objects.get(user = user)
    claim = Claim.objects.get(id = claim_id)
    if account.accountType == 'Claims':
        if request.method == "POST":
            claim.approval = request.POST['approval']
            claim.save()
            return HttpResponseRedirect(reverse("claim:claims"))
        
        return render(request, "claim/claimsDetail.html", {"claim":claim})
    return render(request, "claim/login.html")

def doctorsList(request):
    return render(request, "claim/doctorsList.html")


def addDoctor(request):
    return render(request, "claim/addDoctor.html")
    


    
def doctorHomeUpdate(request, claim_id):
    user = request.user
    account = Account.objects.get(user = user)
    oldClaim = Claim.objects.get(id =claim_id)
    print(oldClaim)
    
    if account.accountType == 'Doctor':
        
        if request.method == "POST":
            claim = request.POST["claim"]
            tariff = request.POST["tariff"]
            age = request.POST["age"]
            practice = request.POST["practice"]
            gender = request.POST["gender"]
            if gender == "M":
                genderNo = 0
            else:
                genderNo = 1
            description = request.POST["description"]
            if description == "PAEDIATRICIANS":
                descriptionNo = 0
            else:
                descriptionNo = 1

            svm_pred = svm_job.predict([[age, genderNo, claim, practice, descriptionNo, tariff]])[0]
            knn_pred = knn_job.predict([[age, genderNo, claim, practice, descriptionNo, tariff]])[0]
            logistic_pred = logistic_job.predict([[age, genderNo, claim, practice, descriptionNo, tariff]])[0]
            gauss_pred = gauss_job.predict([[age, genderNo, claim, practice, descriptionNo, tariff]])[0]
            svm_pred = svm_job.predict([[age, genderNo, claim, practice, descriptionNo, tariff]])[0]
            trees_pred = trees_job.predict([[age, genderNo, claim, practice, descriptionNo, tariff]])[0]
            forest_pred = forest_job.predict([[age, genderNo, claim, practice, descriptionNo, tariff]])[0]
            if knn_pred == 0:
                knn_pred = "Proceed"
            else:
                knn_pred = "Possible Fraud"
            if svm_pred == 1:
                svm_pred = "Proceed"
            else:
                svm_pred = "Possible Fraud"
            if logistic_pred == 1:
                logistic_pred = "Proceed"
            else:
                logistic_pred = "Possible Fraud"
            if gauss_pred == 1:
                gauss_pred = "Proceed"
            else:
                gauss_pred = "Possible Fraud"
            if trees_pred == 1:
                trees_pred = "Proceed"
            else:
                trees_pred = "Possible Fraud"
            if forest_pred == 1:
                forest_pred = "Proceed"
            else:
                forest_pred = "Possible Fraud"

            oldClaim.doctor = account 
            oldClaim.claimed = claim 
            oldClaim.age = age
            oldClaim.gender = gender
            oldClaim.practice = practice
            oldClaim.description = description
            oldClaim.tariff = tariff
            oldClaim.approval = "Pending"
            oldClaim.knn = knn_pred
            oldClaim.svm = svm_pred
            oldClaim.logistics = logistic_pred
            oldClaim.bayes = gauss_pred
            oldClaim.forest = forest_pred
            oldClaim.trees = trees_pred
            oldClaim.save()

            return HttpResponseRedirect(reverse("claim:myclaims"))
            
        return render(request, "claim/myClaimUpdate.html", {"claims":oldClaim})
    return render(request, "claim/login.html")