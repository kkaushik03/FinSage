from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'score/index.html')  # Render the HTML template

def hello_world(request):
    return HttpResponse("Hello World")  # Return "Hello World"