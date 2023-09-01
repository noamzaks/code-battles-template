"""
Basic type hints for JavaScript in PyOdide and PyScript.
A lot of properties are missing.
"""

from typing import Callable, Literal, Optional

from pyodide.ffi import JsCallable

class TwoDContext:
    textAlign: Literal["left", "right", "center", "start", "end"]
    textBaseline: Literal[
        "top", "hanging", "middle", "alphabetic", "ideographic", "bottom"
    ]
    font: str
    fillStyle: str

    @staticmethod
    def fillText(text: str, x: int, y: int):
        pass
    @staticmethod
    def fillRect(x: int, y: int, width: int, height: int):
        pass
    @staticmethod
    def drawImage(image: Image, x: int, y: int, width: int, height: int):
        pass
    @staticmethod
    def clearRect(startX: int, endX: int, width: int, height: int):
        pass
    @staticmethod
    def save():
        pass
    @staticmethod
    def restore():
        pass
    @staticmethod
    def translate(x: float, y: float):
        pass
    @staticmethod
    def rotate(radians: float):
        pass

class Styles:
    width: str
    height: str
    display: str

class Element:
    id: str
    value: str
    textContent: str
    ariaValueNow: str
    onclick: JsCallable
    width: float
    height: float
    clientWidth: Optional[int]
    clientHeight: Optional[int]
    style: Styles

    @staticmethod
    def getContext(dimensions: str) -> TwoDContext:
        pass
    @staticmethod
    def click():
        pass
    @staticmethod
    def getElementsByClassName(classname: str) -> HTMLCollection:
        pass

class document:
    body: Element

    @staticmethod
    def getElementById(id: str) -> Element:
        pass

class Matches:
    matches: bool

class Event:
    pass

class window:
    devicePixelRatio: float

    @staticmethod
    def matchMedia(media: str) -> Matches:
        pass
    @staticmethod
    def addEventListener(listener: JsCallable) -> int:
        pass

class Audio:
    @staticmethod
    def new(src: str) -> Audio:
        pass
    @staticmethod
    def cloneNode(p: bool) -> Audio:
        pass
    @staticmethod
    def play() -> None:
        pass

class HTMLCollection:
    @staticmethod
    def to_py() -> list[Element]:
        pass

class Image(Element):
    @staticmethod
    def new() -> Image:
        pass
    src: str
    onload: Callable[[Event], None]
    onerror: Callable[[Event], None]

def clearInterval(id: int) -> None:
    pass

def setInterval(fn: JsCallable, period: int) -> int:
    pass

def clearInterval(id: int):
    pass

def setTimeout(fn: JsCallable, period: int) -> None:
    pass

class FontFace:
    @staticmethod
    def new(name: str, url: str):
        pass
    @staticmethod
    def load():
        pass
