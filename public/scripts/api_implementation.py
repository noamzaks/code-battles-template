"""
The API implementation of the game.
This class should be a complete implementation of the Context
class defined in the api file.
It has access to the game's state, and can change it accordingly.
It also has access to its player's index.
"""

from api import *
from game_state import GameState
from web_utilities import console_log


class GameContext(Context):
    _game: GameState
    _player_index: int

    def __init__(self, game: GameState, player_index: int) -> None:
        self._game = game
        self._player_index = player_index

    ### API IMPLEMENTATION ###

    def log_info(self, text: str):
        console_log(
            self._player_index,
            f"[INFO {str(self._game.time).rjust(8)}s] {text}",
            "#f8f8f2",
        )

    def log_warning(self, text: str):
        console_log(
            self._player_index,
            f"[WARNING {str(self._game.time).rjust(5)}s] {text}",
            "#f1fa8c",
        )

    def log_error(self, text: str):
        console_log(
            self._player_index,
            f"[ERROR {str(self._game.time).rjust(7)}s] {text}",
            "#ff5555",
        )
