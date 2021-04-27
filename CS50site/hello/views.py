from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, "hello/index.html")


def Me(request):
    return HttpResponse("Hello Ryan!")


def NotMe(request):
    return HttpResponse("You are not I!")


def greet(request, name):
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })
