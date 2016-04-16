from FaceSoundLink import *
from random import randint

class Brain():
    def __init__(self):
        self.State = "neutral"
        self.Anim = NeutralFace()
        self.change_state = False  
        
    def RandomState(self):
        newState = "neutral"
        dice = randint(0,7)
        if(dice == 0):
            newState = "happy"
            self.Anim = HappyFace()
        if(dice == 1):
            newState = "neutral"
            self.Anim = NeutralFace()
        if(dice == 2):
            newState = "sad"
            self.Anim = SadFace()
        if(dice == 3):
            newState = "angry"
            self.Anim = AngryFace()
        if(dice == 4):
            newState = "sleepy"
            self.Anim = SleepyFace()
        if(dice == 5):
            newState = "love"
            self.Anim = LoveFace()
        if(dice == 6):
            newState = "message"
            self.Anim = MessageFace()
        if(dice == 7):
            newState = "batterie"
            self.Anim = BatterieFace()
        
        if(not(newState == self.State)):
            self.State = newState
            self.change_state = True
        else:
            self.change_state = False