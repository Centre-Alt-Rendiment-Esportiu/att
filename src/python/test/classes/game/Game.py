from test.classes.game.BallHistory import BallHistory
from test.classes.game.Player import Player


class Game:
    def __init__(self, args):
        self.players = [Player()] * 2
        self.current_player = 0

        self.ball_history = BallHistory(args["size"])

    def update_history(self, center):
        if center:
            if self.ball_history.check_direction_change(center):
                self.ball_history.change_direction()
                self.change_player()
            self.ball_history.add_ball(center)

    def clear_history(self):
        self.ball_history.clear_history()
        for player in self.players:
            player.reset_score()

    def change_player(self):
        self.current_player = 1 - self.current_player

    def add_score(self):
        self.players[self.current_player].add_score()