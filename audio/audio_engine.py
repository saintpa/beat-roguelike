import pygame


pygame.mixer.init()


def load_sound(path):
    return pygame.mixer.Sound(path)


def play_sound(sound):
    if sound:
        sound.play()
