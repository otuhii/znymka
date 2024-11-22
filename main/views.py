from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required



def indexPage(request):
    return render(request, 'index/index.html')


def homepageView(request):
    if not request.user.is_authenticated:
        return redirect('loginView')
    
    return render(request, 'home/home.html')

def helpPage(request):
    return render(request, "help.html")

#AUTHENTICATION
@csrf_exempt    
def loginView(request):
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
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("loginView") 
    else:
        form = UserCreationForm()

    return render(request, 'signup/signup.html', {
        'form': form #Поміняти цю форму
        })

@login_required
def logout_view(request):
    logout(request)
    return redirect("indexPage")

###################################################


