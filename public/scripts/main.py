import api
from api_implementation import APIImplementation
from code_battles import CodeBattles, run_game
from game_state import GameState


class BattleSnake(CodeBattles[GameState, APIImplementation, type(api)]):
    async def setup(self):
        pass

    def render(self) -> None:
        self.canvas.clear()

        for player_index in range(len(self.player_names)):
            self.canvas.draw_text(
                self.player_names[player_index],
                "black",
                player_index,
                self.map_image.width / 2,
                100,
            )

        self.canvas.draw_text(
            "Frame: " + str(int(self.step)),
            "black",
            0,
            self.canvas.total_width / 2,
            self.map_image.height + 160,
        )

    def simulate_step(self) -> None:
        pass

    def create_initial_state(self):
        return GameState(len(self.player_names))

    def get_api(self):
        return api

    def create_game_context(self, player_index: int):
        return APIImplementation(self.state, player_index)

    def get_extra_height(self):
        return 180

    def get_steps_per_second(self):
        return 20

    def get_board_count(self):
        return 1


if __name__ == "__main__":
    run_game(BattleSnake())
