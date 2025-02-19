from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("U are login successful")
    return HttpResponse("u are not login successful")