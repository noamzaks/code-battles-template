"""
Welcome to the API Documentation!

You probably want to get started with `Context` methods, and have a look at `Exceptions`.
"""

from enum import Enum


class Exceptions(Enum):
    """
    An enum representing result of API methods.
    See each method for a list of possible exceptions.
    If a method was successful, it always returns `OK`.
    """

    OK = 0

    def __bool__(self):
        return self == Exceptions.OK


class API:
    """
    The main access point for your bot. Access this using `self.context` inside your `run` method.

    Each action method returns `Exceptions`, which is `Exceptions.OK` if it succeeded, or another value explaining why it failed.
    """

    ### GENERAL METHODS ###

    def log_info(self, text: str):
        """
        Prints the text to the console as an info message.
        WARNING: Writing to log every time the run method might slow down the game.
        """
        raise NotImplementedError("Log")

    def log_warning(self, text: str):
        """
        Prints the text to the console as a warning.
        WARNING: Writing to log every time the run method might slow down the game.
        """
        raise NotImplementedError("Log")

    def log_error(self, text: str):
        """
        Prints the text to the console as an error.
        WARNING: Writing to log every time the run method might slow down the game.
        """
        raise NotImplementedError("Log")

    def __init__(self) -> None:
        pass


class CodeBattlesBot:
    """
    Base class for writing your bots.

    **Important:** Your bot must subclass this directly, and be called MyBot!

    **Important:** Your bot must not have a custom __init__ method. Use `setup` for any setup code you may have.

    **Example:**

    ```python
    class MyBot(CodeBattlesBot):
        def setup(self):
            self.message = "Hello!"
        def run(self):
            print(self.context)
    ```
    """

    context: API

    def __init__(self, context: API):
        self.context = context
        self.setup()

    def setup(self) -> None:
        """
        This optional method will be called upon construction.

        If you need to define any instance variables like in a constructor, do it here.
        """

    def run(self) -> None:
        """
        This method will be called once every game step.

        Interact with the game using `self.context`.
        """
