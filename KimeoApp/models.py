from django.db import models
from datetime import datetime

class Message(object):
    def __init__(self, robotId, content, created=None):
        self.robotId = robotId
        self.content = content
        self.created = created or datetime.now()

message = Message(robotId=0, content='happyFace')

