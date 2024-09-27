"""
The state class of the game.
In this class, there must be all of the information required to render the game
and also to know what will be the next state of the game, when a step is simulated.
For example, there must be some variables which are set from the user APIs,
and variables corresponding to the position of every game object.
"""


class PlayerState:
    pass


class GameState:
    players: list[PlayerState]

    def __init__(self, players: int):
        self.players = [PlayerState() for _ in range(players)]
