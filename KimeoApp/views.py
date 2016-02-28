from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about-project.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def actions(request):
    return render(request, 'actions.html')

def movement(request):
    return render(request, 'movement.html')

def message(request):
    return render(request, 'message.html')

def monitoring(request):
    return render(request, 'monitoring.html')

def blog(request):
    return render(request, 'blog.html')

def contact(request):
    return render(request, 'contact.html')
