import api
from api_implementation import APIImplementation, PlayerRequests
from code_battles import CodeBattles, run_game
from game_state import GameState


class MyCodeBattles(CodeBattles[GameState, APIImplementation, type(api), PlayerRequests]):
    async def setup(self):
        pass

    def render(self):
        self.canvas.clear()

        for player_index in range(len(self.player_names)):
            self.canvas.draw_text(
                self.player_names[player_index],
                self.map_image.width / 2,
                self.map_image.height + 70,
                board_index=player_index,
                text_size=40
            )

        self.canvas.draw_text(
            "Frame: " + str(int(self.step)),
            self.canvas.total_width / 2,
            self.map_image.height + 120,
            text_size=40
        )

    def make_decisions(self) -> bytes:
        if self.step == 10:
            return b"1"
        
        return b"0"

    def apply_decisions(self, decisions: bytes):
        for player_index in self.active_players:
            self.run_bot_method(player_index, "run")

            if decisions == b"1":
                self.eliminate_player(player_index, "Game is not implemented yet!")

    def create_initial_state(self):
        return GameState(len(self.player_names))

    def create_initial_player_requests(self, player_index: int):
        return PlayerRequests()

    def get_api(self):
        return api

    def create_api_implementation(self, player_index: int):
        return APIImplementation(player_index, self.state, self.player_requests[player_index])

    def configure_board_count(self) -> int:
        return len(self.player_names)

    def configure_extra_height(self):
        return 180

    def configure_steps_per_second(self):
        return 20


if __name__ == "__main__":
    run_game(MyCodeBattles())
