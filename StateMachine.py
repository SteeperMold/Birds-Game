from dataclasses import dataclass
from enum import Enum


class GameState(Enum):
    UNKNOWN = "unknown"
    INITIALIZING = "initializing"
    INITIALIZED = "initialized"
    MAIN_MENU = "main_menu"
    MAIN_LEVEL_PLAYING = "main_level_playing"
    IM_A_BIRD_LEVEL_PLAYING = "im_a_bird_level_playing"
    RECORDS_TABLE_MENU = "records_table_menu"
    QUITTING = "quitting"


class StateError(Exception):
    """
    Вызывается, если игра оказывается в непредвиденном состоянии.
    Например, при попытке начать игру, когда она еще не иницализирована.
    """


@dataclass
class StateMachine:
    state: GameState

    def set_state(self, new_state):
        self.state = new_state

    def assert_state_is(self, *expected_states: GameState):
        """Проверяет, находится ли игра в одом из `expected_states`. В противном случае вызывает `StateError`."""

        if self.state not in expected_states:
            raise StateError(f"Игра должна быть в одном из {expected_states}, а не {self.state}")
