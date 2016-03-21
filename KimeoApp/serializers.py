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
        fields = ('direction', 'rightSpeed', 'leftSpeed', 'duration')
