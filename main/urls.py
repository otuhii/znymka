from django.urls import path

from . import views

urlpatterns = [
    path("", views.indexPage, name="indexPage"),
    path("home/", views.homepageView, name="homepageView"),
    path("login/", views.loginView, name="loginView"),
    path("signup/", views.signupView, name="signupView"),
    path("help/", views.helpPage, name="helpPage"),
    #path('profile/<str:username>/', views.view_profile, name='view_profile'),
    #path("uploadPhoto/<str:username>/", views.uploadphoto, name="uploadPhoto"),
    #path("logout/", views.logout_view, name="logout_view"),
]