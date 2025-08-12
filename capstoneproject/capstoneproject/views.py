# from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    return render(request, 'home.html')

def profile(request):
    return render(request, 'profile.html')


