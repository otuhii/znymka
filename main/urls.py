from django.urls import path
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    path("", views.indexPage, name="indexPage"),
    path("home/", views.homepageView, name="homepageView"),
    path("login/", views.loginView, name="loginView"),
    path("help/", views.helpPage, name="helpPage"),
    path("signup/", views.signupView, name="signupView"),
    path("logout/", views.logoutView, name="logoutView"),
    path('<str:username>/', views.viewProfile, name='viewProfile'),
    path('<str:username>/friends', views.friends, name="usersFriends"),
    path('<str:username>/addfriend', views.addFriend, name="addFriend"),
    path("<str:username>/uploadphoto", views.uploadPhoto, name="uploadPhoto"),


]
