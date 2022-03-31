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
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        userId = User
        message = "Incorrect username or password."
        if user is not None:
            account = Account.objects.get(user = user)
            #print(user)
            account_name = account.name
            #print (account.accountType)
            if user is not None and account.accountType == 'Doctor':
                login(request, user)
                return HttpResponseRedirect(reverse("claim:doctor"))
            else:
                return render(request, "claim/login.html", {"message":"Account is for Claims."})
    return render(request, "claim/login.html", {"message":message})

def claimsLogin(request):
    #return render(request, 'claim/login.html')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        message = "Incorrect username or password."
        if user is not None:
            account = Account.objects.get(user = user)
            if user is not None and account.accountType == 'Claims':
                login(request, user)
                return HttpResponseRedirect(reverse("claim:claims"))
            else:
                return render(request, "claim/login.html", {"message":"Account is for Doctor."})
    return render(request, "claim/login.html", {"message":message})

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
            member = request.POST["member"]
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

            newClaim = Claim.objects.create(doctor=account, member= member, claimed=claim, age=age, gender=gender, practice=practice, description=description, tariff=tariff, approval="Pending", knn=knn_pred, svm=svm_pred, logistics=logistic_pred, bayes=gauss_pred, forest=forest_pred, trees=trees_pred)
            newClaim.save()
            return HttpResponseRedirect(reverse("claim:myclaims"))
        return render(request, "claim/doctorHome.html", {"account": account})
    return render(request, "claim/login.html")

def myClaims(request):
    user = request.user
    account = Account.objects.get(user = user)
    if account.accountType == 'Doctor':
        claims = Claim.objects.filter(doctor = account)
        return render(request, "claim/myClaims.html", {'claims':claims, 'account':account})
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
    user = request.user
    account = Account.objects.get(user = user)
    if account.accountType == 'Claims':
        doctors = Account.objects.filter(accountType = 'Doctor')
        return render(request, "claim/doctorsList.html", {"doctors":doctors})
    return render(request, "claim/login.html")

def addDoctor(request):
    user = request.user
    account = Account.objects.get(user = user)
    if account.accountType == 'Claims':
        if request.method == "POST":
            name = request.POST["name"]
            department = request.POST["department"]
            username = request.POST["username"]
            password = request.POST["password"]
            picture = request.FILES["picture"]
            new_user = User.objects.create_user(username, password=password)
            new_user.save()
            doctor = Account.objects.create(user = new_user, accountType='Doctor', display_picture=picture, name=name, department=department, username=username) 
            doctor.save()
            return HttpResponseRedirect(reverse("claim:doctors-list"))
        return render(request, "claim/addDoctor.html")
    return render(request, "claim/login.html")

def doctorUpdate(request, doctor_id):
    user = request.user
    account = Account.objects.get(user = user)
    oldDoctor = Account.objects.get(id = doctor_id)
    accountUser = oldDoctor.user
    if account.accountType == 'Claims':
        if request.method == "POST":
            name = request.POST["name"]
            department = request.POST["department"]
            username = request.POST["username"]
            password = request.POST["password"]

            for key in request.FILES:
                if key == 'picture':

                    oldDoctor.display_picture = request.FILES[key]
                   


            
           # print(type(request.FILES.picture))
            #if  request.POST.picture  == '':
             #   picture = ''
            #else:
             #   picture = request.FILES["picture"]
              #  oldDoctor.picture = picture
           
            oldDoctor.name = name
            oldDoctor.department = department
            oldDoctor.username = username

            accountUser.username = username

            accountUser.save()
            
            oldDoctor.save()
            return HttpResponseRedirect(reverse("claim:doctors-list"))
        return render(request, "claim/doctorUpdate.html", {"doctor":oldDoctor} )
    return render(request, "claim/login.html")

def doctorHomeUpdate(request, claim_id):
    user = request.user
    account = Account.objects.get(user = user)
    oldClaim = Claim.objects.get(id =claim_id)
    
    if account.accountType == 'Doctor':
        
        if request.method == "POST":
            claim = request.POST["claim"]
            tariff = request.POST["tariff"]
            age = request.POST["age"]
            practice = request.POST["practice"]
            gender = request.POST["gender"]
            member = request.POST["member"]
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
            oldClaim.member = member
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
            
        return render(request, "claim/myClaimUpdate.html", {"claims":oldClaim, 'account':account})
    return render(request, "claim/login.html")