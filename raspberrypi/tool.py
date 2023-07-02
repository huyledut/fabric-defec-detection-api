from gtts import gTTS
import os
import pygame
from time import sleep

pygame.init()
def Read(defects):
    if not defects:
        pygame.mixer.music.load("None.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            sleep(0.1)
        return
    defects.insert(0, 'Detect')
    while defects:
        pygame.mixer.music.load(f"{defects.pop(0)}.mp3")
        pygame.mixer.music.play()
        print("Dang phat am thannh")
        while pygame.mixer.music.get_busy():
            sleep(0.1)