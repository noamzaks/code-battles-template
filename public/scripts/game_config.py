"""
Main game configuration
"""

from api_implementation import GameContext
from game_renderer import render
from game_simulator import simulate_step
from game_state import GameState


async def initial_setup(player_names: list[str]):
    """
    Performs additional setup for the simulation,
    and returns additional arguments to render the game
    """

    return []


def create_initial_state(player_count: int, map: str):
    return GameState(player_count)


def create_context(game_state: GameState, player_index: int):
    return GameContext(game_state, player_index)


CONFIGURATION = {
    "render": render,
    "simulate_step": simulate_step,
    "create_initial_state": create_initial_state,
    "initial_setup": initial_setup,
    "create_context": create_context,
    "extra_height": 180,
}
