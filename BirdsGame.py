from dataclasses import dataclass, field
from typing import Tuple

import pygame

import GameLoops
from StateMachine import StateMachine, GameState


@dataclass
class BirdsGame:
    screen: pygame.Surface
    width: int = field(init=False, default=1280)
    height: int = field(init=False, default=720)
    size: Tuple[int, int] = field(init=False, default=(1280, 720))
    fullscreen: bool
    state_machine: StateMachine
    clock: pygame.time.Clock = field(init=False, default=None)
    all_sprites: pygame.sprite.Group = field(init=False, default=None)
    main_menu: GameLoops.MainMenuLoop = field(init=False, default=None)

    @classmethod
    def create(cls, fullscreen=False):
        game = cls(
            screen=None,
            fullscreen=fullscreen,
            state_machine=StateMachine(GameState.INITIALIZING)
        )
        game.init()
        return game

    def init(self):
        self.state_machine.assert_state_is(GameState.INITIALIZING)

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

        self.main_menu = GameLoops.MainMenuLoop(game=self)

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
                pass
            elif self.state_machine.state == GameState.IM_A_BIRD_LEVEL_PLAYING:
                pass
            elif self.state_machine.state == GameState.RECORDS_TABLE_MENU:
                pass

        pygame.quit()
