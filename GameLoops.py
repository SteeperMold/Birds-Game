import random
from dataclasses import dataclass, field
from typing import Any

import pygame

from StateMachine import GameState


class CustomEvents:
    DIFFICULTY_CHANGE = pygame.USEREVENT + 1
    ADD_SCORE = pygame.USEREVENT + 2
    OBSTACLE_SPAWN = pygame.USEREVENT + 3
    BIRD_SPAWN = pygame.USEREVENT + 4


@dataclass
class GameLoop:
    game: Any
    initialized: bool = field(init=False, default=False)

    def reset(self):
        self.initialized = False

    def start(self):
        """
        Выполняет первоначальную настройку уровня, например инициализацию спрайтов.
        """

    def update(self):
        """
        Вызывается каждый кадр.
        """

    def handle_event(self, event):
        """
        Обрабатывает одиночный ивент.
        """

    def loop(self):
        if not self.initialized:
            self.start()
            self.initialized = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_state(GameState.QUITTING)

            self.handle_event(event)

        self.update()

    # Методы для удобства
    def set_state(self, new_state: GameState):
        self.game.state_machine.set_state(new_state)

    @property
    def state(self) -> GameState:
        return self.game.state_machine.state

    @property
    def all_sprites(self) -> pygame.sprite.Group:
        return self.game.all_sprites

    @property
    def obstacle_sprites(self) -> pygame.sprite.Group:
        return self.game.obstacle_sprites

    @property
    def birds_sprites(self) -> pygame.sprite.Group:
        return self.game.birds_sprites

    @property
    def bullet_booster_sprites(self) -> pygame.sprite.Group:
        return self.game.bullet_booster_sprites

    @property
    def health_booster_sprites(self) -> pygame.sprite.Group:
        return self.game.health_booster_sprites

    @property
    def width(self) -> int:
        return self.game.width

    @property
    def height(self) -> int:
        return self.game.height

    @property
    def screen(self) -> pygame.Surface:
        return self.game.screen

    @property
    def clock(self) -> pygame.time.Clock:
        return self.game.clock


class MainMenuLoop(GameLoop):
    def __init__(self, game):
        super().__init__(game)
        self.play_btn = None
        self.bird_mode_btn = None
        self.records_btn = None
        self.exit_menu_btn = None

    def start(self):
        import Sprites
        self.all_sprites.empty()
        Sprites.MainMenuBackground(self.all_sprites)
        Sprites.CloudsSprite(self.all_sprites, x=140, y=120)
        Sprites.PlayerSprite(self.all_sprites, x=90, y=300)
        Sprites.BirdSprite(self.all_sprites, x=960, y=200)
        Sprites.GameNameSprite(self.all_sprites, x=364, y=10)

        self.play_btn = Sprites.PlayButton(self.all_sprites, x=370, y=250)
        self.bird_mode_btn = Sprites.BirdModeButton(self.all_sprites, x=370, y=370)
        self.records_btn = Sprites.RecordsButton(self.all_sprites, x=370, y=490)
        self.exit_menu_btn = Sprites.ExitMenuButton(self.all_sprites, x=370, y=610)

    def update(self):
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if self.play_btn.rect.collidepoint(mouse_pos):
                self.set_state(GameState.MAIN_LEVEL_PLAYING)

            elif self.bird_mode_btn.rect.collidepoint(mouse_pos):
                self.set_state(GameState.IM_A_BIRD_LEVEL_PLAYING)

            elif self.records_btn.rect.collidepoint(mouse_pos):
                self.set_state(GameState.RECORDS_TABLE_MENU)

            elif self.exit_menu_btn.rect.collidepoint(mouse_pos):
                self.set_state(GameState.QUITTING)


class MainGameLoop(GameLoop):
    def __init__(self, game):
        super().__init__(game)
        self.difficulty = 0
        self.health = 0
        self.score = 0
        self.bullets = 0
        self.game_over = False
        self.player = None
        self.heart_sprites = None
        self.font = None
        self.score_sprite = None

    def start(self):
        pygame.time.set_timer(CustomEvents.OBSTACLE_SPAWN, 1000)
        pygame.time.set_timer(CustomEvents.BIRD_SPAWN, 1500)
        pygame.time.set_timer(CustomEvents.DIFFICULTY_CHANGE, 5000)
        pygame.time.set_timer(CustomEvents.ADD_SCORE, 1500)

        self.difficulty = 20
        self.health = 3
        self.score = 0
        self.bullets = 5
        self.game_over = False
        self.font = pygame.font.Font(None, 70)

        self.all_sprites.empty()
        from Sprites import GroundSprite, AnimatedPlayerSprite, HeartSprite, ScoreSprite, BulletIcon
        GroundSprite(self.all_sprites, x=0, y=550)
        BulletIcon(self.all_sprites, x=400, y=15)
        self.score_sprite = ScoreSprite(self.all_sprites, x=self.width - 100, y=10)
        self.player = AnimatedPlayerSprite(self.all_sprites, x=100, y=320)
        self.heart_sprites = [HeartSprite(self.all_sprites, x=20 + i * 100, y=10) for i in range(self.health)]

    def update(self):
        self.screen.fill("#88b0ed")

        if not self.game_over:
            self.all_sprites.update()

        score_text = self.font.render(f'{self.score}', True, '#ffe7bd')
        self.screen.blit(score_text, (self.width - score_text.get_width() - 20, 20))
        self.score_sprite.move(self.width, score_text.get_width())

        bullets_text = self.font.render(f'{self.bullets}', True, '#ffe7bd')
        self.screen.blit(bullets_text, (470, 25))

        if pygame.sprite.spritecollide(self.player, self.obstacle_sprites, True, pygame.sprite.collide_mask):
            self.health -= 1
            self.heart_sprites.pop().kill()

            if self.health == 0:
                self.game_over = True

        if pygame.sprite.spritecollide(self.player, self.bullet_booster_sprites, True, pygame.sprite.collide_mask):
            self.bullets += 1

        if pygame.sprite.spritecollide(self.player, self.health_booster_sprites, True, pygame.sprite.collide_mask):
            self.health = min(self.health + 1, 3)
            if len(self.heart_sprites) < self.health:
                from Sprites import HeartSprite
                self.heart_sprites = [HeartSprite(self.all_sprites, x=20 + i * 100, y=10) for i in range(self.health)]

        self.all_sprites.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(60)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.player.jump()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.bullets > 0:
            self.bullets -= 1
            from Sprites import BulletSprite
            BulletSprite(
                self.all_sprites,
                x=self.player.rect.centerx + 80, y=self.player.rect.centery - 23,
                birds_sprite_group=self.birds_sprites
            )

        elif event.type == CustomEvents.OBSTACLE_SPAWN:
            if random.randint(0, 100) <= 10:
                from Sprites import BulletBoosterSprite
                BulletBoosterSprite(
                    self.all_sprites, self.bullet_booster_sprites,
                    x=self.width, y=540,
                    move_speed=max(self.difficulty // 10, 5)
                )
            elif random.randint(0, 100) <= 5:
                from Sprites import HealthBoosterSprite
                HealthBoosterSprite(
                    self.all_sprites, self.health_booster_sprites,
                    x=self.width, y=510,
                    move_speed=max(self.difficulty // 10, 5)
                )
            elif random.randint(0, 100) < self.difficulty:
                from Sprites import ObstacleSprite
                ObstacleSprite(
                    self.all_sprites, self.obstacle_sprites,
                    x=self.width, y=515,
                    move_speed=max(self.difficulty // 10, 5)
                )

        elif event.type == CustomEvents.BIRD_SPAWN:
            if random.randint(0, 100) < self.difficulty:
                from Sprites import MovingBirdSprite
                MovingBirdSprite(
                    self.all_sprites, self.obstacle_sprites, self.birds_sprites,
                    x=self.width, y=150,
                    move_speed=max(self.difficulty // 10, 5)
                )

        elif event.type == CustomEvents.DIFFICULTY_CHANGE:
            self.difficulty = min(self.difficulty + 1, 100)

        elif event.type == CustomEvents.ADD_SCORE and not self.game_over:
            self.score += 1
