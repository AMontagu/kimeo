from pygame import mixer


def playSound(fileName, repeat):
    for r in range(repeat):
        mixer.init()
        mixer.music.load(fileName)
        mixer.music.play()
        while mixer.music.get_busy() == True:
            continue


if __name__ == '__main__':
    playSound("bird.wav", 2)