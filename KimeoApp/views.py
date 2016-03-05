from django.http import HttpResponse
import django
from kimeo.settings import *
from django.shortcuts import render
from django.core.mail import send_mail
from KimeoApp.forms import ContactForm
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

def control(request):
    return render(request, 'control.html')

def monitoring(request):
    return render(request, 'monitoring.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():

            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            send_mail(subject, name + 'Sent you a message \n\n' + message, email, fail_silently=False)

            send = True
    else:
        form = ContactForm()

    return render(request, 'contact.html', locals())



def mail(request):
    subject = request.GET['subject']
    email = request.GET['email']
    name = request.GET['name']
    message = request.GET['message']
    send_mail(subject, name + 'Sent you a message \n\n' + message, email,
    ['adrienmontagu@gmail.com'], fail_silently=False)
    return render(request, 'contact.html')