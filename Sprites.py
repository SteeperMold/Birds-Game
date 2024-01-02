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
    apply_mask = False

    def __init__(self, *group, x=0, y=0):
        super().__init__(*group)
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        if self.apply_mask:
            self.mask = pygame.mask.from_surface(self.image)


class BaseAnimatedSprite(pygame.sprite.Sprite):
    sheet = None
    columns = rows = 0
    animation_speed = 0
    apply_mask = False

    def __init__(self, *group, x=0, y=0):
        super().__init__(*group)
        self.frames = []
        self.cut_sheet()
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.last_animation_update = 0
        if self.apply_mask:
            self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self):
        self.rect = pygame.Rect(0, 0, self.sheet.get_width() // self.columns, self.sheet.get_height() // self.rows)

        for j in range(self.rows):
            for i in range(self.columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(self.sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        if pygame.time.get_ticks() - self.last_animation_update > 1000 / self.animation_speed:
            self.last_animation_update = pygame.time.get_ticks()
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            if self.apply_mask:
                self.mask = pygame.mask.from_surface(self.image)


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


class GroundSprite(BaseSprite):
    image = load_image("ground.png")


class ObstacleSprite(BaseSprite):
    image = load_image("obstacle.png")
    apply_mask = True

    def __init__(self, *group, x=0, y=0, move_speed=5):
        super().__init__(*group, x=x, y=y)
        self.move_speed = move_speed

    def update(self):
        self.rect.x -= self.move_speed
        if self.rect.x < -self.rect.w:
            self.kill()


class MovingBirdSprite(BaseSprite):
    image = load_image("Bird.png")
    apply_mask = True

    def __init__(self, *group, x=0, y=0, move_speed=5):
        super().__init__(*group, x=x, y=y)
        self.move_speed = move_speed

    def update(self):
        self.rect.x -= self.move_speed
        if self.rect.x < -self.rect.w:
            self.kill()


class HeartSprite(BaseSprite):
    image = load_image("heart.png")


class ScoreSprite(BaseSprite):
    image = load_image('score.png')

    def move(self, screen_width, text_width):
        self.rect.x = screen_width - text_width - 100


class BulletSprite(BaseSprite):
    image = load_image('bullet.png')

    def __init__(self, *group, x=0, y=0, birds_sprite_group):
        super().__init__(*group, x=x, y=y)
        self.birds_sprite_group = birds_sprite_group

    def update(self):
        self.rect.x += 10
        if (pygame.sprite.spritecollide(self, self.birds_sprite_group, True, pygame.sprite.collide_mask) or
                self.rect.x > 1280 - self.rect.w):
            self.kill()


class BulletIcon(BaseSprite):
    image = load_image('bullet_icon.png')


class BulletBoosterSprite(BaseSprite):
    image = load_image('bullet_booster.png')

    def __init__(self, *group, x=0, y=0, move_speed=5):
        super().__init__(*group, x=x, y=y)
        self.move_speed = move_speed

    def update(self):
        self.rect.x -= self.move_speed
        if self.rect.x < -self.rect.w:
            self.kill()


class HealthBoosterSprite(BaseSprite):
    image = load_image('health_booster.png')
    apply_mask = True

    def __init__(self, *group, x=0, y=0, move_speed=5):
        super().__init__(*group, x=x, y=y)
        self.move_speed = move_speed

    def update(self):
        self.rect.x -= self.move_speed
        if self.rect.x < -self.rect.w:
            self.kill()


class AnimatedPlayerSprite(BaseAnimatedSprite):
    sheet = load_image("animated_player.png")
    columns = 4
    rows = 1
    animation_speed = 20
    jump_height = 4
    apply_mask = True

    def __init__(self, *group, x=0, y=0):
        super().__init__(*group, x=x, y=y)
        self.is_jumping = False
        self.jump_frames = 25

    def update(self):
        if not self.is_jumping:
            super().update()
            return

        if self.jump_frames >= -25:
            self.rect.y -= round(self.jump_frames * abs(self.jump_frames) * self.jump_height / 100)
            self.jump_frames -= 1
        else:
            self.jump_frames = 25
            self.is_jumping = False

    def jump(self):
        self.is_jumping = True
        self.image = self.frames[0]
        self.mask = pygame.mask.from_surface(self.image)


class PlayButton(BaseSprite):
    image = load_image("play_btn.png")


class BirdModeButton(BaseSprite):
    image = load_image("bird_mode_btn.png")


class ExitMenuButton(BaseSprite):
    image = load_image("exit_btn.png")


class RecordsButton(BaseSprite):
    image = load_image("records_btn.png")
