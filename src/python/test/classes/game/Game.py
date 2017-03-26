from test.classes.game.BallHistory import BallHistory
from test.classes.game.Player import Player


class Game:
    def __init__(self, args):
        self.players = (Player(), Player())
        self.current_player = 0
        self.bounces = 0
        self.ball_history = BallHistory(args["size"])
        self.table_points = None

    def set_table(self, table_points):
        self.table_points = table_points

    def update_history(self, center):
        if center:
            if self.ball_history.check_direction_change(center):
                self.check_point()
                self.change_player()
            if self.ball_history.has_bounced(center):
                self.bounces += 1
            self.ball_history.update_history(center)

    def clear_history(self):
        self.ball_history.clear_history()
        for player in self.players:
            player.reset_score()
        self.current_player = 0
        self.bounces = 0

    def change_player(self):
        self.current_player = 1 - self.current_player
        self.bounces = 0

    # TODO Fix check_point algorithm - Should take into account table
    def check_point(self):
        if self.bounces > 2:
            self.players[self.current_player].add_score()
