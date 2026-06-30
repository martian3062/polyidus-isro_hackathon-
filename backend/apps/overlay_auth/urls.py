from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register,      name="overlay-register"),
    path("login/",    views.login_verify,  name="overlay-login"),
]
