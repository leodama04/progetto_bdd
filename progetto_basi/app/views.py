from django.shortcuts import render, HttpResponse

def home(request):
    return HttpResponse("Hello, world! This is the home page.")