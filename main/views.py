from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout






def indexPage(request):
    return render(request, 'index/index.html')




def homepageView(request):
    if not request.user.is_authenticated:
        return redirect('loginView')
    
    return render(request, 'home/home.html')

def helpPage(request):
    return render(request, "help.html")


#AUTHENTICATION
def loginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request=request, username=username, password=password)
        if user != None:
            login(request, user)
            return redirect('homepageView')
        else:
            return redirect('indexPage')

    return render(request, 'login/login.html')

def signupView(request):
    pass




#############################################