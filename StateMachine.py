from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple, Set


class GameState(Enum):
    UNKNOWN = "unknown"
    INITIALIZING = "initializing"
    INITIALIZED = "initialized"
    MAIN_MENU = "main_menu"
    MAIN_LEVEL_PLAYING = "main_level_playing"
    IM_A_BIRD_LEVEL_PLAYING = "im_a_bird_level_playing"
    RECORDS_TABLE_MENU = "records_table_menu"
    QUITTING = "quitting"
    GAME_OVER = "game_over"
    PAUSE_MENU = "pause_menu"


class StateError(Exception):
    """
    Вызывается, если игра оказывается в непредвиденном состоянии.
    Например, при попытке начать игру, когда она еще не иницализирована.
    """


@dataclass
class StateMachine:
    game_loops: Tuple
    state: GameState = field(default=GameState.UNKNOWN)
    previous_states: Set[GameState] = field(default_factory=set)

    def set_state(self, new_state, **kwargs):
        for game_loop in self.game_loops:

            for previous_state in self.previous_states:
                if game_loop.linked_game_state == previous_state:
                    game_loop.reset()

            if game_loop.linked_game_state == new_state:
                game_loop.set_presets(kwargs)

        self.state = new_state
        self.previous_states.add(new_state)

    def assert_state_is(self, *expected_states: GameState):
        """
        Проверяет, находится ли игра в одом из `expected_states`. В противном случае вызывает `StateError`.
        """

        if self.state not in expected_states:
            raise StateError(f"Игра должна быть в одном из {expected_states}, а не {self.state}")
