from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


def indexPage(request):
    if request.user.is_authenticated:
        return redirect('homepageView') 
    

    return render(request, 'index/index.html')


def homepageView(request):
    if not request.user.is_authenticated:
        return redirect('loginView')    


    '''
    мені треба зробити функцію яка буде вибирати друзів користувача, брати всі їхні пости і вибирати тільки ті які виставили за останню добу, якщо таких нема - просто
    не повертати нічого 
    '''


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



#я би переглянув ще раз цю функції, треба переробити і доробити!!!!!!!!!!!
@login_required
def friends(request, username):
    is_own_profile = request.user.username == username

    friendsList = request.user.profile.friends.all()


    #Вилючаємо з цих профілів зареєстрованого користувача і його друзів
    recommendedProfiles = User.objects.exclude(
        id__in=[request.user.id] + list(friendsList.values_list('user__id', flat=True))
    )[:5]#перші п'ять захаркоджених користувачів
    #потім можна додати якийсь пошук за дейксрою або можливо по номеру телефону шукати

    if is_own_profile:
        return render(request, "friendsPage/page.html", {
            "profile": request.user.profile,
            "friends_list": friendsList,  
            "recommendedProfiles": recommendedProfiles,
        })


    return render(request, "help.html")



#треба доробити щоб не остаточно додавало друга а просто надсилало йому запит на дружбу
@login_required
def addFriend(request, username):
    try:
        isFriend = request.user.profile.isFriend(username)
        if not isFriend:
            friendUser = get_object_or_404(User, username=username)
            friendProfile = friendUser.profile

            request.user.profile.friends.add(friendProfile)

        return redirect('usersFriends', username=request.user.username)



    except User.DoesNotExist:
        messages.error(request, 'Користувача не знайдено')
        return redirect('usersFriends', username=request.user.username)
    