import sqlite3
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

    game_loops: Tuple = field(init=False, default_factory=tuple)

    @classmethod
    def create(cls, fullscreen=False):
        game = cls(
            screen=None,
            fullscreen=fullscreen,
        )
        game.init()
        return game

    def init(self):
        self.game_loops = (
            GameLoops.MainMenuLoop(game=self),
            GameLoops.MainGameLoop(game=self),
            GameLoops.GameOver(game=self),
            GameLoops.PauseMenu(game=self),
            GameLoops.RecordsTableLoop(game=self),
        )

        self.state_machine = StateMachine(self.game_loops, GameState.INITIALIZING)

        connection = sqlite3.connect('leaderboard.sqlite')
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS main_level (
            score INTEGER
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS im_a_bird_level (
            score INTEGER
        )""")

        connection.commit()
        connection.close()

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
            for game_loop in self.game_loops:
                if game_loop.linked_game_state == self.state_machine.state:
                    game_loop.loop()

        pygame.quit()
