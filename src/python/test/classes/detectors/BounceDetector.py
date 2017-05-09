import numpy as np

from test.classes.utils.Ball import Ball
from test.classes.utils.BallHistory import BallHistory

LEN_HISTORY_BOUNCE = 4
RESIDUE_THRESHOLD = 1


class BounceDetector:
    @staticmethod
    def find_bounce(history):
        # If we don't have enough points to find bounce, return None
        if len(history) < LEN_HISTORY_BOUNCE + 1:
            return Ball()

        # Fit a parabola through last MIN_HISTORY_BOUNCE points
        last_balls = list(history)[-LEN_HISTORY_BOUNCE:]
        x_val = np.array([p.center[0] for p in last_balls])
        y_val = np.array([p.center[1] for p in last_balls])
        _pol, res, _rank, _sing, _rcond = np.polyfit(x_val, y_val, 2, full=True)

        # If the quadratic residue of fitted parabola is high
        # It means our points are not fitting well through a parabola anymore
        # Meaning there has been a change (bounce) in between
        if res > RESIDUE_THRESHOLD:
            # TODO If we are in the beginning, the bounce needs not necessarily be in where I found it

            # Since we have detected bounce AFTER it happened
            # To find coordinates, we have to go back one in history
            # Pass a parabola through those points and find coordinates
            last_balls_without_last = list(history)[-LEN_HISTORY_BOUNCE - 1:-1]
            x_val = np.array([p.center[0] for p in last_balls_without_last])
            y_val = np.array([p.center[1] for p in last_balls_without_last])
            pol = np.polyfit(x_val, y_val, 2, full=False)  # We don't need quadratic residue

            # For minimizing the error, consider it as between last 2 points
            # TODO if post-processed, intersect parabolas of before and after
            center_x = (history[-1].center[0] + history[-2].center[0]) / 2
            center_y = np.polyval(pol, center_x)

            bounce_ball = Ball((center_x, center_y))
            bounce_ball.is_bounce = True
            return bounce_ball
        return Ball()
