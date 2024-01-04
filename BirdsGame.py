from dataclasses import dataclass, field
from typing import Tuple

import pygame

import GameLoops
from StateMachine import StateMachine, GameState


@dataclass
class BirdsGame:
    screen: pygame.Surface
    fullscreen: bool

    width: int = field(init=False, default=1280)
    height: int = field(init=False, default=720)
    size: Tuple[int, int] = field(init=False, default=(1280, 720))

    state_machine: StateMachine = field(init=False, default=None)
    clock: pygame.time.Clock = field(init=False, default=None)

    all_sprites: pygame.sprite.Group = field(init=False, default=None)
    obstacle_sprites: pygame.sprite.Group = field(init=False, default=None)
    birds_sprites: pygame.sprite.Group = field(init=False, default=None)
    bullet_booster_sprites: pygame.sprite.Group = field(init=False, default=None)
    health_booster_sprites: pygame.sprite.Group = field(init=False, default=None)

    main_menu: GameLoops.MainMenuLoop = field(init=False, default=None)
    main_level: GameLoops.MainGameLoop = field(init=False, default=None)
    game_over: GameLoops.GameOver = field(init=False, default=None)
    pause_menu: GameLoops.PauseMenu = field(init=False, default=None)

    @classmethod
    def create(cls, fullscreen=False):
        game = cls(
            screen=None,
            fullscreen=fullscreen,
        )
        game.init()
        return game

    def init(self):
        self.main_menu = GameLoops.MainMenuLoop(game=self)
        self.main_level = GameLoops.MainGameLoop(game=self)
        self.game_over = GameLoops.GameOver(game=self)
        self.pause_menu = GameLoops.PauseMenu(game=self)

        self.state_machine = StateMachine(self.main_menu, self.main_level, self.game_over, self.pause_menu,
                                          GameState.INITIALIZING)

        pygame.init()
        window_style = pygame.FULLSCREEN if self.fullscreen else 0
        bit_depth = pygame.display.mode_ok(self.size, window_style, 32)
        self.screen = pygame.display.set_mode(self.size, window_style, bit_depth)

        pygame.mixer.pre_init(
            frequency=44100,
            size=32,
            channels=2,
            buffer=512,
        )

        pygame.font.init()

        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.birds_sprites = pygame.sprite.Group()
        self.bullet_booster_sprites = pygame.sprite.Group()
        self.health_booster_sprites = pygame.sprite.Group()

        self.state_machine.set_state(GameState.INITIALIZED)

    def start_game(self):
        self.state_machine.assert_state_is(GameState.INITIALIZED)
        self.state_machine.set_state(GameState.MAIN_MENU)
        self.loop()

    def loop(self):
        while self.state_machine.state != GameState.QUITTING:
            if self.state_machine.state == GameState.MAIN_MENU:
                self.main_menu.loop()
            elif self.state_machine.state == GameState.MAIN_LEVEL_PLAYING:
                self.main_level.loop()
            elif self.state_machine.state == GameState.IM_A_BIRD_LEVEL_PLAYING:
                pass
            elif self.state_machine.state == GameState.RECORDS_TABLE_MENU:
                pass
            elif self.state_machine.state == GameState.GAME_OVER:
                self.game_over.loop()
            elif self.state_machine.state == GameState.PAUSE_MENU:
                self.pause_menu.loop()

        pygame.quit()
