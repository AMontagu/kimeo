from pygame import mixer
import time

repo = "/home/pi/Desktop/Kimeo/kimeo/soundControl/sonKimeo/"
def playSound(fileName, repeat=1):
    for r in range(repeat):
        try:
          mixer.init()
        except:
          return
        sound = mixer.Sound(repo + fileName)
        sound.play()
        while mixer.music.get_busy() == True:
            continue


if __name__ == '__main__':
    playSound("../bird.wav", 2)
    time.sleep(2)
