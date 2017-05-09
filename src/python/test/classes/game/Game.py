import cv2
import numpy as np

from test.classes.game.Player import Player
from test.classes.utils.BallHistory import BallHistory


class Game:
    def __init__(self, args):
        self.players = (Player(), Player())
        self.current_player = 0
        self.bounces = [0, 0]
        self.ball_history = BallHistory(args["size"])
        self.left_table = None
        self.right_table = None

    def set_table(self, table_points):
        # 0 -> upper left corner
        # 1 -> upper right corner
        # 2 -> lower right corner
        # 3 -> lower left corner
        upper_middle_point = (table_points[0] + table_points[1]) / 2
        lower_middle_point = (table_points[2] + table_points[3]) / 2
        l_table = np.array([table_points[0], upper_middle_point, lower_middle_point, table_points[3]])
        r_table = np.array([upper_middle_point, table_points[1], table_points[2], lower_middle_point])
        self.left_table = l_table.astype(int)
        self.right_table = r_table.astype(int)

    def update_history(self, center):
        if not center:
            return

        if self.ball_history.check_direction_change(center):
            self.check_point()
            self.change_player()

        bounce_point = self.ball_history.has_bounced(center)
        if bounce_point:
            in_left = cv2.pointPolygonTest(self.left_table, bounce_point, False)
            if in_left >= 0:
                self.bounces[0] += 1
            else:
                in_right = cv2.pointPolygonTest(self.right_table, bounce_point, False)
                if in_right >= 0:
                    self.bounces[1] += 1

        self.ball_history.update_history(center)

    # TODO Should take into account servings
    def check_point(self):
        # If it bounced on my side, point for other player
        if self.bounces[self.current_player] > 0:
            self.players[1 - self.current_player].add_score()
        # If it bounced more than once on other side, point for me
        if self.bounces[1 - self.current_player] > 1:
            self.players[self.current_player].add_score()

    def change_player(self):
        self.current_player = 1 - self.current_player
        self.bounces = [0, 0]

    def clear_history(self):
        self.ball_history.clear_history()
        for player in self.players:
            player.reset_score()
        self.current_player = 0
        self.bounces = [0, 0]
