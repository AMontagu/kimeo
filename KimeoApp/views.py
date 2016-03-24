from django.db.models import Count
from django.http import HttpResponse
import django
from kimeo.settings import *
from django.shortcuts import render
from django.core.mail import send_mail
from KimeoApp.forms import ContactForm

from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from django.http import Http404
from KimeoApp.serializers import *
from KimeoApp.models import *
from KimeoApp.RobotCommunication import *
from rest_framework.decorators import api_view

### ------------- Navigation views -----------------------------
def home(request):
    print("home")
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
    #tryData = Sound.objects.all().annotate(numSound = Count('soundName')) # get all sound even it's same soundName
    #tryData = Sound.objects.values('soundName').distinct().count() #get only the number of distinct value
    #tryData = Sound.objects.values('soundName').distinct() # get sound distinct but without number
    #tryData = Sound.objects.annotate(numSound = Count('soundName')) # get all sound even it's same soundName
    tryData = Sound.objects.values('soundName').annotate(numSound = Count('soundName')) # return list of sound name with associated value
    for sound in tryData:
        print(sound['soundName'])
        print(sound['numSound'])
    return render(request, 'monitoring.html', locals())

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

"""class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer"""

class MessageList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        message = Message.objects.all()
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            robotCommunication = RobotCommunication()
            robotCommunication.receiveMessage(serializer);
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageDetail(APIView):
    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        message = self.get_object(pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        message = self.get_object(pk)
        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        message = self.get_object(pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# --------------------------- Move part -------------------

class MovementList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        movement = Movement.objects.all()
        serializer = MovementSerializer(movement, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MovementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            robotCommunication = RobotCommunication()
            robotCommunication.move(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovementDetail(APIView):
    def get_object(self, pk):
        try:
            return Movement.objects.get(pk=pk)
        except Movement.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        movement = self.get_object(pk)
        serializer = MovementSerializer(movement)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        movement = self.get_object(pk)
        serializer = MovementSerializer(movement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        movement = self.get_object(pk)
        movement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------------- Sound part -------------------

class SoundList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        sound = Sound.objects.all()
        serializer = SoundSerializer(sound, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SoundSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            robotCommunication = RobotCommunication()
            robotCommunication.makeSound(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SoundDetail(APIView):
    def get_object(self, pk):
        try:
            return Sound.objects.get(pk=pk)
        except Sound.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        sound = self.get_object(pk)
        serializer = SoundSerializer(sound)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        sound = self.get_object(pk)
        serializer = SoundSerializer(sound, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        sound = self.get_object(pk)
        sound.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------------- Sound part -------------------

class LightList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        light = Light.objects.all()
        serializer = LightSerializer(light, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            robotCommunication = RobotCommunication()
            robotCommunication.makeLight(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LightDetail(APIView):
    def get_object(self, pk):
        try:
            return Light.objects.get(pk=pk)
        except Light.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        light = self.get_object(pk)
        serializer = LightSerializer(light)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        light = self.get_object(pk)
        serializer = LightSerializer(light, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        light = self.get_object(pk)
        light.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------------- Screen part -------------------

class ScreentList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        screen = Screen.objects.all()
        serializer = ScreenSerializer(screen, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ScreenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            robotCommunication = RobotCommunication()
            robotCommunication.changeRobotFace(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScreenDetail(APIView):
    def get_object(self, pk):
        try:
            return Screen.objects.get(pk=pk)
        except Screen.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        screen = self.get_object(pk)
        serializer = ScreenSerializer(screen)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        screen = self.get_object(pk)
        serializer = ScreenSerializer(screen, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        screen = self.get_object(pk)
        screen.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)