from django.http import HttpResponse
import django
from kimeo.settings import *
from django.shortcuts import render
from django.core.mail import send_mail
from KimeoApp.forms import ContactForm

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from KimeoApp.serializers import UserSerializer, GroupSerializer

### ------------- Navigation views -----------------------------
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

            send_mail(subject, name + ' Sent you a message \n\n' + message + '\n\n email to respond : ' + email , 'contact.kimeo@gmail.com', ['contact.kimeo@gmail.com'], fail_silently=False)

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



### ------------------ API PART---------------------------------

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer