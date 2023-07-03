"""
The simulation method of the game.
This method should take a state of the game and change it to the next one.
It is not responsible for running the Player APIs, but the Player APIs
are run immediately before it and should keep information in the game state.
"""

from game_state import GameState


def simulate_step(state: GameState, player_names: list[str]) -> None:
    state.steps += 1
