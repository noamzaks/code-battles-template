"""
The API implementation of the game.
This class should be a complete implementation of the Context
class defined in the api file.
It has access to the game's state, and can change it accordingly.
It also has access to its player's index.
"""

from api import *
from game_state import GameState


class GameContext(Context):
    _game: GameState
    _player_index: int

    def __init__(self, game: GameState, player_index: int) -> None:
        self._game = game
        self._player_index = player_index

    ### API IMPLEMENTATION ###
