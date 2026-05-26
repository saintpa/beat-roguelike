import pygame

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)

pygame.mixer.init()

pygame.mixer.set_num_channels(64)


def load_sound(path):
    return pygame.mixer.Sound(path)


def play_sound(sound):
    if sound:
        channel = pygame.mixer.find_channel(force=True)
        if channel:
            channel.play(sound)

