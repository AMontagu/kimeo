from django.db import models


class Message(models.Model):
    robotId = models.IntegerField()
    userName = models.CharField(max_length=100)
    content = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Creation Date")

#message = Message(robotId=0, userName="test", content='happyFace')

