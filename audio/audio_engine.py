import pygame

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.init()
pygame.mixer.set_num_channels(64)


def load_sound(path):
    return pygame.mixer.Sound(path)


def get_channel(channel_id):
    return pygame.mixer.Channel(channel_id)


def play_sound_on_channel(sound, channel):
    if not sound:
        return

    channel.stop()
    channel.play(sound)


def stop_channel(channel):
    if channel:
        channel.stop()

