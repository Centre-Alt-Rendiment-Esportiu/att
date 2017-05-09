import numpy as np

from test.classes.utils.Ball import Ball
from test.classes.utils.BallHistory import BallHistory

MIN_HISTORY_BOUNCE = 4
RESIDUE_THRESHOLD = 1


class BounceDetector:
    def __init__(self):
        self.ball_queue = BallHistory(tail_size=8)

    def add_ball(self, ball):
        self.ball_queue.update_history(ball)

    def find_bounce(self):
        # If we don't have enough points to find bounce, return None
        if len(self.ball_queue) < MIN_HISTORY_BOUNCE + 1:
            return None

        # Fit a parabola through last MIN_HISTORY_BOUNCE points
        last_balls = list(self.ball_queue)[-MIN_HISTORY_BOUNCE:]
        x_val = np.array([p.center[0] for p in last_balls])
        y_val = np.array([p.center[1] for p in last_balls])
        _pol, res, _rank, _sing, _rcond = np.polyfit(x_val, y_val, 2, full=True)

        # If the quadratic residue of fitted parabola is high
        # It means our points are not fitting well through a parabola anymore
        # Meaning there has been a change (bounce) in between
        if res > RESIDUE_THRESHOLD:
            # TODO If we are in the beginning, the bounce needs not necessarily be in where I found it

            # Since we have detected bounce AFTER it happened
            # To find coordinates, we have to go back to one in history
            # Pass a parabola through those points and find coordinates
            last_balls_without_last = list(self.ball_queue)[-MIN_HISTORY_BOUNCE - 1:-1]
            x_val = np.array([p.center[0] for p in last_balls_without_last])
            y_val = np.array([p.center[1] for p in last_balls_without_last])
            pol = np.polyfit(x_val, y_val, 2, full=False)  # We don't need quadratic residue

            # For minimizing the error, consider it as between last 2 points of deque
            # TODO if post-processed, intersect parabolas of before and after
            center_x = (self.ball_queue[-1].center[0] + self.ball_queue[-2].center[0]) / 2
            center_y = np.polyval(pol, center_x)

            last_point = self.ball_queue[-1]
            self.clear()
            self.add_ball(last_point)

            bounce_ball = Ball(tuple([center_x, center_y]))
            bounce_ball.is_bounce = True
            return bounce_ball
        return None

    def find_bounce2(self):
        if len(self.ball_queue) < MIN_HISTORY_BOUNCE + 1:
            return

        last_balls_without_last = list(self.ball_queue)[-MIN_HISTORY_BOUNCE - 1:-1]
        x_val = np.array([p.center[0] for p in last_balls_without_last])
        y_val = np.array([p.center[1] for p in last_balls_without_last])
        pol = np.polyfit(x_val, y_val, 2, full=False)

        x1, y1 = self.ball_queue[-1].center
        x2 = self.ball_queue[-2].center[0]
        y2 = int(np.rint(np.polyval(pol, x1)))

        if abs(y1 - y2) > 0.3 * abs(x1 - x2):
            center_x = int(np.rint(x1 + x2) / 2)
            center_y = int(np.rint(np.polyval(pol, center_x)))

            last_point = self.ball_queue[-1]
            self.clear()
            self.add_ball(last_point)

            bounce_ball = Ball(tuple([center_x, center_y]))
            bounce_ball.is_bounce = True
            return bounce_ball
        return None

    def clear(self):
        self.ball_queue.clear_history()
