from django.db import models


class Message(models.Model):
    robotId = models.IntegerField()
    userName = models.CharField(max_length=100)
    content = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Creation Date")

class Movement(models.Model):
    direction = models.CharField(max_length=100) #type of movement : forward, backward, left, right
    rightSpeed = models.IntegerField()
    leftSpeed = models.IntegerField()
    duration = models.IntegerField()

class Light(models.Model):
    turnOn = models.BooleanField()  #true if light turn on
    blink = models.BooleanField() #true if light is blinking
    repeat = models.IntegerField() #number of blinking repetition
    intervalBlinking = models.IntegerField() # Time between turn on and turn off

class Sound(models.Model):
    soundName = models.CharField(max_length=100) #name of sound file like sound.mp3
    repeat = models.IntegerField() #number of sound repetition

class Screen(models.Model):
    imageName = models.CharField(max_length=100)  # Id of image on screen
    stay = models.BooleanField() #true if the image called stay until other request
    timeToStay = models.IntegerField() # if stay is false, time for display image on screen

