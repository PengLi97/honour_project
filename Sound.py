import pygame

class Sound:

    def click():
        pygame.mixer.init()
        pygame.mixer.music.load('music/click.mp3')
        pygame.mixer.music.play()

    def bomb():
        pygame.mixer.init()
        pygame.mixer.music.load('music/bomb.mp3')
        pygame.mixer.music.play()

    def background(i):
        pygame.mixer.init()
        pygame.mixer.music.load('music/background.mp3')
        if i == 1:
            pygame.mixer.music.play()
        elif i == 0:
            pygame.mixer.music.pause()
        else:
            pass
    def sortcard():
        pygame.mixer.init()
        pygame.mixer.music.load('music/sortcard.mp3')
        pygame.mixer.music.play()

    def cardShove():
        pygame.mixer.init()
        pygame.mixer.music.load('music/cardShove.mp3')
        pygame.mixer.music.play()

    def passToNext():
        pygame.mixer.init()
        pygame.mixer.music.load('music/pass.mp3')
        pygame.mixer.music.play()

    def winMusic():
        pygame.mixer.init()
        pygame.mixer.music.load('music/win.mp3')
        pygame.mixer.music.play()

    def loseMusic():
        pygame.mixer.init()
        pygame.mixer.music.load('music/lose.mp3')
        pygame.mixer.music.play()


