from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def indexPage(request):
    if request.user.is_authenticated:
        return redirect('homepageView') 
    

    return render(request, 'index/index.html')


def homepageView(request):
    if not request.user.is_authenticated:
        return redirect('loginView')    

    return render(request, 'home/home.html', {
        "user" : request.user,
        "profile" : request.user.profile,
        "friendsCount" : request.user.profile.friends.all().count(),
    })

def helpPage(request):
    return render(request, "help.html")



#AUTHENTICATION
@csrf_exempt    
def loginView(request):
    if request.user.is_authenticated:
        return redirect('homepageView') 

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        #phoneNum = request.POST["phoneNum"]
        user = authenticate(request=request, username=username, password=password)
        if user != None:
            login(request, user)
            return redirect('homepageView')
        else:
            return redirect('indexPage')

    return render(request, 'login/login.html')

@csrf_exempt
def signupView(request):
    if request.user.is_authenticated:
        return redirect('homepageView')

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("loginView") 
    else:
        form = UserCreationForm()

    return render(request, 'signup/signup.html', {
        'form': form 
        })

@login_required
def logoutView(request):
    logout(request)
    return redirect("indexPage")

###################################################


@login_required
def viewProfile(request, username):
    user_profile = get_object_or_404(User, username=username).profile
    is_own_profile = request.user.username == username

    return render(request, "profile/profilePage.html",{
        "profile" : user_profile,
        "isOwn" : is_own_profile
    })

@login_required
def friends(request, username):
    return render(request, "help.html")