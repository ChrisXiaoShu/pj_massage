from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound

def sayhello(request):
    return HttpResponse('Hello Django')

def get_image_test(request, ID):
    return HttpResponseNotFound( ID + "ChrisNotFound")
    

# Create your views here.
