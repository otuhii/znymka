from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.db import models


from .models import ProfilePhoto, Profile

def indexPage(request):
    if request.user.is_authenticated:
        return redirect('homepageView') 
    

    return render(request, 'index/index.html')


def homepageView(request):
    if not request.user.is_authenticated:
        return redirect('loginView')    

    user = request.user
    friends = user.profile.friends.all()
    

    #хароший ефективний спосіб(як мені сказали) отримувати зразу за один запит профілі друзів і їх недавні фото
    recent_threshold = timezone.now() - timedelta(days=1)

    friends_photos = Profile.objects.filter(
        friends=user.profile
    ).prefetch_related(
        models.Prefetch(
            'photos',
            queryset=ProfilePhoto.objects.filter(
                upload_date__gte=recent_threshold,
                is_active=True
            )
        )
    )

    posts = {friend: friend.photos.all() for friend in friends_photos}


    return render(request, 'home/home.html', {
        "user" : user,
        "profile" : user.profile,
        "friendsCount" : user.profile.friends.all().count(),
        "posts" : posts,
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
    photos = user_profile.get_recent_photos('any')

    return render(request, "home/profile/profilePage.html",{
        "profile" : user_profile,
        "isOwn" : is_own_profile,
        "photos" : photos,
    })



#я би переглянув ще раз цю функції, треба переробити і доробити!!!!!!!!!!!
@login_required
def friends(request, username):
    is_own_profile = request.user.username == username


    if is_own_profile:
        friendsList = request.user.profile.friends.all()


        #Вилючаємо з цих профілів зареєстрованого користувача і його друзів і адмінський аккаунт
        recommendedProfiles = User.objects.exclude(
            Q(id__in=[request.user.id] + list(friendsList.values_list('user__id', flat=True))) |
            Q(is_superuser=True)
        )[:5]

        #перші п'ять захаркоджених користувачів
        #потім можна додати якийсь пошук за дейксрою(типу друзі друзів і тд)
        #або можливо по номеру телефону шукати

        
        return render(request, "home/friendsPage/page.html", {
            "profile": request.user.profile,
            "friendsList": friendsList,  
            "recommendedProfiles": recommendedProfiles,
        })


    



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
    


@csrf_exempt
@login_required
def uploadPhoto(request, username):
    if request.method == "POST":
        new_photo = ProfilePhoto.objects.create(
            profile=request.user.profile,
            local_image=request.FILES['photo'],
            photo_type=request.POST.get('photo_type', 'GALLERY'),
            caption=request.POST.get('caption', '')
        )
        new_photo.save()
        return redirect(reverse('viewProfile', kwargs={'username': request.user.username}))