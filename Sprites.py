import os
import sys

import pygame


def load_image(name, color_key=None):
    fullname = os.path.join('assets', 'images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class BaseSprite(pygame.sprite.Sprite):
    image = None

    def __init__(self, *group, x=0, y=0):
        super().__init__(*group)
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class MainMenuBackground(BaseSprite):
    image = load_image("main_menu_background.png")


class PlayerSprite(BaseSprite):
    image = load_image("player.png")


class GameNameSprite(BaseSprite):
    image = load_image("game_name.png")


class CloudsSprite(BaseSprite):
    image = load_image("clouds.png")


class BirdSprite(BaseSprite):
    image = load_image("bird.png")
