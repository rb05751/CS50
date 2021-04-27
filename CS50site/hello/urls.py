from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.greet, name="greet"),
    path("me", views.Me, name="Me"),
    path("notme", views.NotMe, name="NotMe")
]
