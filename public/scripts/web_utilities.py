"""Generic useful utilities for creating games with PyScript."""

import asyncio
from typing import Callable, Union

import pyscript
from js import Audio, Element, FontFace, Image, document, window


class Alignment:
    CENTER = 0
    TOP_LEFT = 1


def download_image(src: str) -> Image:
    result = asyncio.Future()
    image = Image.new()
    image.onload = lambda _: result.set_result(image)
    image.src = src
    return result


def download_images(sources: list[tuple[str, str]]) -> dict[str, Image]:
    remaining_images: list[str] = []
    result = asyncio.Future()

    images: dict[str, Image] = {}
    remaining = len(sources)

    def add_image(image):
        nonlocal remaining
        nonlocal remaining_images
        src = image.currentTarget.src
        to_remove = None
        for image in remaining_images:
            if image in src:
                to_remove = image
                break
        if to_remove:
            remaining_images.remove(to_remove)

        remaining -= 1
        if remaining == 0:
            result.set_result(images)

    for key, src in sources:
        image = Image.new()
        images[key] = image
        remaining_images.append(src)
        image.onload = lambda _: add_image(_)
        image.onerror = lambda _: print(f"Failed to fetch {src}")
        image.src = src

    return result


def get_element(id: str) -> Element:
    """Wrapper for JS getElementById."""
    return document.getElementById(id)


def get_breakpoint() -> int:
    value = document.getElementById("breakpoint").value
    if value == "":
        return -1
    return int(value)


def show_alert(
    title: str, alert: str, color: str, icon: str, limit_time: int = 5000, is_code=True
):
    if hasattr(window, "showAlert"):
        window.showAlert(title, alert, color, icon, limit_time, is_code)


def set_results(player_names: list[str], places: list[int], map: str):
    if hasattr(window, "setResults"):
        window.setResults(player_names, places, map)


def download_json(filename: str, contents: str):
    if hasattr(window, "downloadJson"):
        window.downloadJson(filename, contents)


def console_log(player_index: int, text: str, color: str):
    if hasattr(window, "consoleLog"):
        window.consoleLog(player_index, text, color)


def should_play():
    return "Pause" in document.getElementById("playpause").textContent


def get_playback_speed():
    return 2 ** float(
        document.getElementById("timescale")
        .getElementsByClassName("mantine-Slider-thumb")
        .to_py()[0]
        .ariaValueNow
    )


SOUNDS: dict[str, Audio] = {}


def play_sound(sound: str):
    if sound not in SOUNDS:
        SOUNDS[sound] = Audio.new("/sounds/" + sound + ".mp3")

    SOUNDS[sound].cloneNode(True).play()


async def with_timeout(fn: Callable[[], None], timeout_seconds: float):
    async def f():
        fn()

    await asyncio.wait_for(f(), timeout_seconds)


class GameCanvas:
    """
    A nice wrapper around HTML Canvas for drawing map-based multiplayer games.
    """

    scale: float
    """The amount of real pixels in one map pixel"""

    def __init__(
        self,
        canvas: Element,
        player_count: int,
        map_image: Image,
        max_width: int,
        max_height: int,
        extra_height: int,
    ):
        self.canvas = canvas
        self.player_count = player_count
        self.map_image = map_image
        self.extra_height = extra_height

        self.fit_into(max_width, max_height)

    def fit_into(self, max_width: int, max_height: int):
        if self.map_image.width == 0 or self.map_image.height == 0:
            raise Exception("Map image invalid!")
        aspect_ratio = (
            self.map_image.width
            * self.player_count
            / (self.map_image.height + self.extra_height)
        )
        width = min(max_width, max_height * aspect_ratio)
        height = width / aspect_ratio
        self.canvas.style.width = f"{width}px"
        self.canvas.style.height = f"{height}px"
        self.canvas.width = width * window.devicePixelRatio
        self.canvas.height = height * window.devicePixelRatio
        self.scale = self.canvas.width / self.player_count / self.map_image.width
        self.context = self.canvas.getContext("2d")
        self.context.textAlign = "center"
        self.context.textBaseline = "middle"

        self.canvas_map_width = self.canvas.width / self.player_count
        self.canvas_map_height = (
            self.canvas_map_width * self.map_image.height / self.map_image.width
        )

    def _translate_position(self, player_index: int, x: float, y: float):
        x *= self.scale
        y *= self.scale
        x += player_index * self.map_image.width * self.scale

        return x, y

    def _translate_width(self, width: float, aspect_ratio: float):
        """Aspect ratio: w/h"""
        width *= self.scale
        height = width / aspect_ratio
        return width, height

    def clear(self):
        """Clears the canvas and re-draws the players' maps"""
        self.context.clearRect(0, 0, self.canvas.width, self.canvas.height)
        self.context.fillStyle = "#fff"
        self.context.fillRect(0, 0, self.canvas.width, self.canvas.height)

        for i in range(self.player_count):
            self.context.drawImage(
                self.map_image,
                i * self.canvas.width / self.player_count,
                0,
                self.map_image.width * self.scale,
                self.map_image.height * self.scale,
            )

    def draw_element(
        self,
        image: Image,
        player_index: int,
        x: int,
        y: int,
        width: int,
        direction: Union[float, None] = None,
        alignment=Alignment.CENTER,
    ):
        """
        Draws the given image on the specified player's board.
        Scaled to fit `width` in map pixels, be on position (`x`, `y`) in map pixels and face `direction`
        where 0 is no rotation and the direction is clockwise positive.
        """

        if direction is None:
            direction = 0

        x, y = self._translate_position(player_index, x, y)
        width, height = self._translate_width(width, image.width / image.height)

        if alignment == Alignment.TOP_LEFT:
            x += width / 2
            y += height / 2

        self.context.save()
        self.context.translate(x, y)
        self.context.rotate(direction)
        self.context.translate(-width / 2, -height / 2)
        self.context.drawImage(image, 0, 0, width, height)
        self.context.restore()

    def draw_text(
        self,
        text: str,
        color: str,
        player_index: int,
        x: int,
        y: int,
        text_size=15,
        font="",
    ):
        if font != "":
            font += ", "

        x, y = self._translate_position(player_index, x, y)
        self.context.font = f"{text_size * self.scale}pt {font}system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif, 'Noto Emoji'"
        self.context.fillStyle = color
        self.context.fillText(text, x, y)

    @property
    def total_width(self):
        return self.map_image.width * self.player_count


async def load_font(name: str, url: str):
    ff = FontFace.new(name, f"url({url})")
    await ff.load()
    document.fonts.add(ff)


class Stub:
    def __init__(self, other):
        for key in dir(other):
            if key.startswith("_"):
                continue
            setattr(
                self,
                key,
                lambda *args, ctt=getattr(other, key), **kwargs: ctt(*args, **kwargs),
            )
