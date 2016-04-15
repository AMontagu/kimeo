from pygame import mixer


def playSound(fileName, repeat=1):
    for r in range(repeat):
        try:
          mixer.init()
        except:
          return
        mixer.music.load(fileName)
        mixer.music.play()
        while mixer.music.get_busy() == True:
            continue


if __name__ == '__main__':
    playSound("bird.wav", 2)
