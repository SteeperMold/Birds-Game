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


class BaseAnimatedSprite(pygame.sprite.Sprite):
    sheet = None
    columns = rows = 0

    def __init__(self, *group, x=0, y=0):
        super().__init__(*group)
        self.frames = []
        self.cut_sheet()
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self):
        self.rect = pygame.Rect(0, 0, self.sheet.get_width() // self.columns, self.sheet.get_height() // self.rows)

        for j in range(self.rows):
            for i in range(self.columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(self.sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class MainMenuBackground(BaseSprite):
    image = load_image("main_menu_background.png")


class PlayerSprite(BaseSprite):
    image = load_image("player.png")


class AnimatedPlayerSprite(BaseAnimatedSprite):
    sheet = load_image("animated_player.png")
    columns = 4
    rows = 2


class GameNameSprite(BaseSprite):
    image = load_image("game_name.png")


class CloudsSprite(BaseSprite):
    image = load_image("clouds.png")


class BirdSprite(BaseSprite):
    image = load_image("bird.png")
