from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.

def home_page(request):
    return render(request, 'home/home.html')