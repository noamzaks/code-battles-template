import asyncio
import math
import time
import traceback

import api
from game_config import CONFIGURATION
from game_state import GameState
from js import Image, clearInterval, document, setInterval, setTimeout, window
from pyodide.ffi import create_once_callable, create_proxy
from web_utilities import (
    GameCanvas,
    Stub,
    download_image,
    get_breakpoint,
    get_playback_speed,
    should_play,
    show_alert,
)

render = CONFIGURATION["render"]
simulate_step = CONFIGURATION["simulate_step"]
create_initial_state = CONFIGURATION["create_initial_state"]
initial_setup = CONFIGURATION["initial_setup"]
create_context = CONFIGURATION["create_context"]


def simulate_with_apis(
    game: GameState,
    player_names: list[str],
    player_globals: list[dict],
):
    simulate_step(game, player_names)
    for index in game.active_player_indices:
        try:
            exec("if player_api is not None: player_api.run()", player_globals[index])
        except:
            lines = traceback.format_exc().splitlines()
            string_file_indices = []
            for i, l in enumerate(lines):
                if "<string>" in l:
                    string_file_indices.append(i)
            output = lines[0] + "\n"
            for i in string_file_indices:
                output += lines[i].strip().replace('File "<string>", l', "L") + "\n"
            output += lines[string_file_indices[-1] + 1].strip() + "\n"

            show_alert(
                f"Code Exception in 'Player {index + 1}' API!",
                output,
                "red",
                "fa-solid fa-exclamation",
            )


def ui_render(
    game_canvas: GameCanvas,
    player_count: int,
    game: GameState,
    player_names: list[str],
    map_image: Image,
    player_globals: list,
    *args,
):
    now = time.time()
    render(game_canvas, player_count, game, player_names, map_image, *args)

    if not game.is_over() and should_play():
        playback_speed = get_playback_speed()
        breakpoint_time = get_breakpoint()
        breakpoint_reached = False
        if playback_speed > 8:
            fraction = int(playback_speed) // 8
            for i in range(fraction):
                if not game.is_over() and not breakpoint_reached:
                    simulate_with_apis(game, player_names, player_globals)
                    if game.time == breakpoint_time:
                        breakpoint_reached = True
                if game.is_over() and should_play():
                    document.getElementById("playpause").click()
            playback_speed /= fraction
        else:
            simulate_with_apis(game, player_names, player_globals)
            if game.is_over() and should_play():
                document.getElementById("playpause").click()
            breakpoint_reached = game.time == breakpoint_time

        if breakpoint_reached:
            if should_play():
                document.getElementById("playpause").click()
        else:
            setTimeout(
                create_once_callable(
                    lambda: ui_render(
                        game_canvas,
                        player_count,
                        game,
                        player_names,
                        map_image,
                        player_globals,
                        *args,
                    )
                ),
                max(50 - (time.time() - now) * 1000, 0) / playback_speed,
            )
    if game.is_over() and should_play():
        document.getElementById("playpause").click()


def start_simulate(
    players: list[str],
    game: GameState,
    player_names: list[str],
    map_image: Image,
    player_globals: list,
    url_params: str,
    *args,
):
    hide_logs = "log=false" in url_params
    player_count = len(players)
    canvas = document.getElementById("simulation")
    game_canvas = GameCanvas(
        canvas,
        player_count,
        map_image,
        document.body.clientWidth - 40
        if hide_logs
        else document.body.clientWidth - 440,
        document.body.clientHeight - 280,
        CONFIGURATION["extra_height"],
    )

    def update_game_canvas(event):
        game_canvas.fit_into(
            document.body.clientWidth - 40
            if hide_logs
            else document.body.clientWidth - 440,
            document.body.clientHeight - 280,
        )
        ui_render(
            game_canvas,
            player_count,
            game,
            player_names,
            map_image,
            player_globals,
            *args,
        )

    window.addEventListener("resize", create_proxy(update_game_canvas))

    document.getElementById("loader").style.display = "none"
    ui_render(
        game_canvas,
        player_count,
        game,
        player_names,
        map_image,
        player_globals,
        *args,
    )

    def step():
        if not game.is_over():
            simulate_with_apis(game, player_names, player_globals)
        ui_render(
            game_canvas,
            player_count,
            game,
            player_names,
            map_image,
            player_globals,
            *args,
        )

    document.getElementById("playpause").onclick = create_proxy(
        lambda _: setTimeout(
            create_proxy(
                lambda: ui_render(
                    game_canvas,
                    player_count,
                    game,
                    player_names,
                    map_image,
                    player_globals,
                    *args,
                )
            ),
            50,
        )
    )
    document.getElementById("step").onclick = create_proxy(
        lambda _: setTimeout(
            create_proxy(step),
            50,
        )
    )


def get_player_apis(game_state: GameState, player_api_code: list[str]) -> list[dict]:
    contexts = [create_context(game_state, i) for i in range(len(player_api_code))]

    player_globals = [
        {
            "math": math,
            "api": api,
            "CodeBattlesBot": api.CodeBattlesBot,
            "player_api": None,
            "context": Stub(context),
            **api.__dict__,
        }
        for context in contexts
    ]
    for index, api_code in enumerate(player_api_code):
        if player_api_code[index] != "":
            if "class MyBot(CodeBattlesBot):" not in api_code:
                show_alert(
                    f"Code Exception in 'Player {index + 1}' API!",
                    "Missing line:\nclass MyBot(CodeBattlesBot):",
                    "red",
                    "fa-solid fa-exclamation",
                )
                continue

            lines = [
                "" if (l.startswith("from") or l.startswith("import")) else l
                for l in api_code.splitlines()
            ]
            lines = "\n".join(lines)
            lines = lines.replace("class MyBot", f"class Player{index}Bot")
            try:
                exec(lines, player_globals[index])
                exec(
                    f"player_api = Player{index}Bot(context)",
                    player_globals[index],
                )
            except:
                lines = traceback.format_exc().splitlines()
                string_file_indices = []
                for i, l in enumerate(lines):
                    if "<string>" in l:
                        string_file_indices.append(i)
                output = lines[0] + "\n"
                for i in string_file_indices:
                    output += lines[i].strip().replace('File "<string>", l', "L") + "\n"
                output += lines[string_file_indices[-1] + 1].strip() + "\n"

                show_alert(
                    f"Code Exception in 'Player {index + 1}' API!",
                    output,
                    "red",
                    "fa-solid fa-exclamation",
                )

    return player_globals


async def simulate_background(
    game: GameState, player_names: list[str], player_apis: list
):
    for _ in range(30):
        simulate_with_apis(game, player_names, player_apis)
        if game.is_over():
            document.getElementById("loader").style.display = "none"
            return

        document.getElementById(
            "loadingText"
        ).textContent = f"Simulating time {game.time}s..."

    setTimeout(
        create_once_callable(
            lambda: simulate_background(game, player_names, player_apis)
        ),
        10,
    )


async def initialize_simulation_async(
    map: str, players: list[str], player_names: list[str], url_params: str
):
    game = create_initial_state(len(players), map)
    player_globals = get_player_apis(game, players)


    map_image = await download_image(
        "/images/maps/" + map.lower().replace(" ", "_") + ".png"
    )

    args = await initial_setup(player_names)

    start_simulate(
        players, game, player_names, map_image, player_globals, url_params, *args
    )


def initialize_simulation(
    map: str, players: list[str], player_names: list[str], url_params: str
):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        initialize_simulation_async(map, players, player_names, url_params)
    )


def run_noui_simulation(map: str, players: list[str], player_names: list[str]):
    game = create_initial_state(len(players), map)
    player_globals = get_player_apis(game, players)
    progress = document.getElementById("noui-progress")
    progress.style.display = "block"

    def step():
        for _ in range(50):
            simulate_with_apis(game, player_names, player_globals)
            if game.is_over():
                progress.style.display = "none"
                clearInterval(window.noUISimulationInterval)
                break
        progress.textContent = f"Simulated {game.time}s"

    window.noUISimulationInterval = setInterval(
        create_proxy(step),
        10,
    )

window.runPython = create_proxy(lambda x: exec(x))