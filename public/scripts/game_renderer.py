"""

"""


from game_state import GameState
from js import Image
from web_utilities import GameCanvas


def render(
    game_canvas: GameCanvas,
    player_count: int,
    game: GameState,
    player_names: list[str],
    map_image: Image,
):
    game_canvas.clear()

    for player_index in range(player_count):
        game_canvas.draw_text(
            player_names[player_index], "black", player_index, map_image.width / 2, 100
        )

    game_canvas.draw_text(
        "Time: " + str(int(game.time)),
        "black",
        0,
        game_canvas.total_width / 2,
        map_image.height + 160,
    )
