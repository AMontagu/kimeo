
repo = "/home/pi/Desktop/Kimeo/kimeo/IHM/resources/FaceGif/CleanFace/"
#repo = "../resources/FaceGif/CleanFace/"
soundrepo = "/home/pi/Desktop/Kimeo/kimeo/soundControl/sonKimeo/"
#soundrepo = "../../soundControl/sonKimeo/"

'''
OtherAnimation

Eye
 Animation("glassesEyes-lookLeft2neutral.gif","glassesEyes-neutral2lookLeft.gif")
 Animation("glassesEyes-lookRight2neutral.gif","glassesEyes-neutral2lookRight.gif")
 Animation("glassesEyes-love.gif","glassesEyes-love.gif")
 Animation("whiteEyes-sleep.gif","whiteEyes-sleep.gif")
 
Mouth
 Animation("whiteMouth-battery.gif","whiteMouth-battery.gif")
 Animation("whiteMouth-happy.gif","whiteMouth-happy.gif")
 Animation("whiteMouth-love.gif","whiteMouth-love.gif")
 Animation("whiteMouth-message2neutral.gif","whiteMouth-neutral2message.gif")
 Animation("whiteMouth-talking.gif","whiteMouth-talking.gif")
 Animation("whiteMouth-talking-slow.gif","whiteMouth-talking-slow.gif")
 
 
Sound

    "angry/angry.ogg"
    "batterie/batterie1.ogg"
    "batterie/batterie2.ogg"
    "batterie/batterie3.ogg"
    "batterie/batterie4.ogg"
    "batterie/batterie5.ogg"
    "call/call1.ogg"
    "happy/happy.ogg"
    "head/head.ogg"
    "message/message1.ogg"
    "message/message2.ogg"
    "message/message3.ogg"
    "message/message4.ogg"
    "message/message5.ogg"
    "message/message6.ogg"
    "message/message7.ogg"
    "ON_OFF/on.ogg"
    "ON_OFF/off.ogg"
    "randomSounds/random1.ogg"
    "randomSounds/random2.ogg"
    "randomSounds/random3.ogg"
    "randomSounds/random4.ogg"
    "randomSounds/random5.ogg"
    "randomSounds/random6.ogg"
    "randomSounds/random7.ogg"
    "randomSounds/random8.ogg"
    "randomSounds/random9.ogg"
    "randomSounds/random10.ogg"
    "randomSounds/random11.ogg"
    "randomSounds/random12.ogg"
    "randomSounds/random13.ogg"
    "randomSounds/random14.ogg"
    "randomSounds/random15.ogg"
    "robotRoule/mouv1.ogg"
    "screenTouch/screen1.ogg"
    "screenTouch/screen3.ogg"
    "screenTouch/screen4.ogg"
    "screenTouch/screen5.ogg"
    "screenTouch/screen6.ogg"
    "screenTouch/screenvalider.ogg"
    "sensor/sensor1.ogg"
    "sensor/sensor2.ogg"
    "sleepMode/sleep.ogg"
    

'''
    
class Animation():
    def __init__(self, TN_name, FN_name):
        str_ = repo + TN_name
        self.TN = str_
        str_ = repo + FN_name 
        self.FN = str_

class AngryFace():
    def __init__(self):
        self.EyeAnim = Animation("glassesEyes-sad2neutral.gif", "glassesEyes-neutral2sad.gif")
        self.MouthAnim = Animation("whiteMouth-troubled2neutral.gif","whiteMouth-neutral2troubled.gif")
        self.SoundAnim = "angry/angry.ogg"
        
        self.EyeAnimation = []
        self.MouthAnimation = [Animation("whiteMouth-talking.gif","whiteMouth-talking.gif"),
                               Animation("whiteMouth-talking-slow.gif","whiteMouth-talking-slow.gif")]
        self.Sound = ["angry/angry.ogg"]
        
class SleepyFace():
    def __init__(self):
        self.EyeAnim = Animation("glassesEyes-closed2neutral.gif", "glassesEyes-neutral2closed.gif")
        self.MouthAnim = Animation("whiteMouth-troubled2neutral.gif","whiteMouth-neutral2troubled.gif")
        self.SoundAnim = "sleepMode/sleep.ogg" 
        self.EyeAnimation = []
        self.MouthAnimation = [Animation("whiteMouth-talking.gif","whiteMouth-talking.gif"),
                               Animation("whiteMouth-talking-slow.gif","whiteMouth-talking-slow.gif")]
        self.Sound = ["sleepMode/sleep.ogg"]

class HappyFace():
    def __init__(self):
        self.EyeAnim = Animation("glassesEyes-love2neutral.gif", "glassesEyes-neutral2love.gif")
        self.MouthAnim = Animation("whiteMouth-happy2neutral.gif","whiteMouth-neutral2happy.gif") 
        self.EyeAnimation = []
        self.MouthAnimation = [Animation("whiteMouth-talking.gif","whiteMouth-talking.gif"),
                               Animation("whiteMouth-talking-slow.gif","whiteMouth-talking-slow.gif")]
        self.Sound = ["happy/happy.ogg",
                    "randomSounds/random1.ogg",
                    "randomSounds/random2.ogg",
                    "randomSounds/random3.ogg",
                    "randomSounds/random4.ogg",
                    "randomSounds/random5.ogg",
                    "randomSounds/random6.ogg",
                    "randomSounds/random7.ogg",
                    "randomSounds/random8.ogg",
                    "randomSounds/random9.ogg",
                    "randomSounds/random10.ogg",
                    "randomSounds/random11.ogg",
                    "randomSounds/random12.ogg",
                    "randomSounds/random13.ogg",
                    "randomSounds/random14.ogg",
                    "randomSounds/random15.ogg"]
        
class SadFace():
    def __init__(self):
        self.EyeAnim = Animation("glassesEyes-sad2neutral.gif", "glassesEyes-neutral2sad.gif")
        self.MouthAnim = Animation("whiteMouth-sad2neutral.gif","whiteMouth-neutral2sad.gif") 
        self.EyeAnimation = []
        self.MouthAnimation = [Animation("whiteMouth-talking.gif","whiteMouth-talking.gif"),
                               Animation("whiteMouth-talking-slow.gif","whiteMouth-talking-slow.gif")]
        self.Sound = ["randomSounds/random1.ogg",
                    "randomSounds/random2.ogg",
                    "randomSounds/random3.ogg",
                    "randomSounds/random4.ogg",
                    "randomSounds/random5.ogg",
                    "randomSounds/random6.ogg",
                    "randomSounds/random7.ogg",
                    "randomSounds/random8.ogg",
                    "randomSounds/random9.ogg",
                    "randomSounds/random10.ogg",
                    "randomSounds/random11.ogg",
                    "randomSounds/random12.ogg",
                    "randomSounds/random13.ogg",
                    "randomSounds/random14.ogg"]
        
class NeutralFace():
    def __init__(self):
        self.EyeAnim = Animation("glassesEyes-neutral.gif", "glassesEyes-neutral.gif")
        self.MouthAnim = Animation("whiteMouth-troubled2neutral.gif","whiteMouth-neutral2troubled.gif") 
        self.EyeAnimation = []
        self.MouthAnimation = [Animation("whiteMouth-talking.gif","whiteMouth-talking.gif"),
                               Animation("whiteMouth-talking-slow.gif","whiteMouth-talking-slow.gif")]
        
        self.Sound = ["randomSounds/random1.ogg",
                    "randomSounds/random2.ogg",
                    "randomSounds/random3.ogg",
                    "randomSounds/random4.ogg",
                    "randomSounds/random5.ogg",
                    "randomSounds/random6.ogg",
                    "randomSounds/random7.ogg",
                    "randomSounds/random8.ogg",
                    "randomSounds/random9.ogg",
                    "randomSounds/random10.ogg",
                    "randomSounds/random11.ogg",
                    "randomSounds/random12.ogg",
                    "randomSounds/random13.ogg",
                    "randomSounds/random14.ogg"]

class LoveFace():
    def __init__(self):
        self.EyeAnim = Animation("glassesEyes-love2neutral.gif", "glassesEyes-neutral2love.gif")
        self.MouthAnim = Animation("whiteMouth-love2neutral.gif","whiteMouth-neutral2love.gif") 
        self.EyeAnimation = []
        self.MouthAnimation = [Animation("whiteMouth-talking.gif","whiteMouth-talking.gif"),
                               Animation("whiteMouth-talking-slow.gif","whiteMouth-talking-slow.gif")]
        self.Sound = ["randomSounds/random1.ogg",
                    "randomSounds/random2.ogg",
                    "randomSounds/random3.ogg",
                    "randomSounds/random4.ogg",
                    "randomSounds/random5.ogg",
                    "randomSounds/random6.ogg",
                    "randomSounds/random7.ogg",
                    "randomSounds/random8.ogg",
                    "randomSounds/random9.ogg",
                    "randomSounds/random10.ogg",
                    "randomSounds/random11.ogg",
                    "randomSounds/random12.ogg",
                    "randomSounds/random13.ogg",
                    "randomSounds/random14.ogg"]

class MessageFace():
    def __init__(self):
        self.EyeAnim = Animation("glassesEyes-neutral.gif", "glassesEyes-neutral.gif")
        self.MouthAnim = Animation("whiteMouth-message2neutral.gif","whiteMouth-neutral2message.gif") 
        self.EyeAnimation = []
        self.MouthAnimation = [Animation("whiteMouth-talking.gif","whiteMouth-talking.gif"),
                               Animation("whiteMouth-talking-slow.gif","whiteMouth-talking-slow.gif")]
        self.Sound = ["message/message1.ogg",
                    "message/message2.ogg",
                    "message/message3.ogg",
                    "message/message4.ogg",
                    "message/message5.ogg",
                    "message/message6.ogg",
                    "message/message7.ogg"]

class BatterieFace():
    def __init__(self):
        self.EyeAnim = Animation("glassesEyes-neutral.gif", "glassesEyes-neutral.gif")
        self.MouthAnim = Animation("whiteMouth-battery2neutral.gif","whiteMouth-neutral2battery.gif") 
        self.EyeAnimation = []
        self.MouthAnimation = [Animation("whiteMouth-talking.gif","whiteMouth-talking.gif"),
                               Animation("whiteMouth-talking-slow.gif","whiteMouth-talking-slow.gif")]
        self.Sound = ["batterie/batterie1.ogg",
                    "batterie/batterie2.ogg",
                    "batterie/batterie3.ogg",
                    "batterie/batterie4.ogg",
                    "batterie/batterie5.ogg",
                    "randomSounds/random1.ogg",
                    "randomSounds/random2.ogg",
                    "randomSounds/random3.ogg",
                    "randomSounds/random4.ogg",
                    "randomSounds/random5.ogg",
                    "randomSounds/random6.ogg",
                    "randomSounds/random7.ogg",
                    "randomSounds/random8.ogg",
                    "randomSounds/random9.ogg",
                    "randomSounds/random10.ogg",
                    "randomSounds/random11.ogg",
                    "randomSounds/random12.ogg",
                    "randomSounds/random13.ogg",
                    "randomSounds/random14.ogg",
                    "randomSounds/random15.ogg"]