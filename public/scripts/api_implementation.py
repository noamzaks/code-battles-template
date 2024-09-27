"""
The API implementation of the game.
This class should be a complete implementation of the Context
class defined in the api file.
It has access to the game's state, that should be thought of as read-only.
It has write access to the corresponding PlayerRequests object, which is then given to the make_decisions and apply_decisions to change the GameState.
It also has access to its player's index.
"""

from api import API
from game_state import GameState


class PlayerRequests:
    pass


class APIImplementation(API):
    _player_index: int
    _state: GameState
    _requests: PlayerRequests

    def __init__(self, player_index: int, state: GameState, requests: PlayerRequests) -> None:
        self._player_index = player_index
        self._state = state
        self._requests = requests

    ### API IMPLEMENTATION ###

    