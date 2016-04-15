from django.contrib.auth.models import User, Group
from rest_framework import serializers
from KimeoApp.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('robotId', 'userName', 'content', 'created')


class MovementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movement
        fields = ('direction', 'rightSpeed', 'leftSpeed', 'headPosition', 'duration', 'continu')


class LightSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Light
        fields = ('turnOn', 'blink', 'repeat', 'intervalBlinking')


class SoundSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sound
        fields = ('soundName', 'repeat')


class ScreenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Screen
        fields = ('imageName', 'stay', 'timeToStay')