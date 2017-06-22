import numpy as np
import warnings

from test.classes.utils.Ball import Ball

LEN_HISTORY_BOUNCE = 4
RESIDUE_THRESHOLD = 0.6


class BounceCalculator:
    def find_bounce(self, history):
        # If we don't have enough points to find bounce, return None
        if len(history) < LEN_HISTORY_BOUNCE:
            return Ball()

        # Fit a parabola through last LEN_HISTORY_BOUNCE points
        last_balls = list(history)[-LEN_HISTORY_BOUNCE:]
        x_val = np.array([p.center[0] for p in last_balls])
        y_val = np.array([p.center[1] for p in last_balls])
        _pol, res, _rank, _sing, _rcond = np.polyfit(x_val, y_val, 2, full=True)

        # If the quadratic residue of fitted parabola is high
        # It means our points are not fitting well through a parabola anymore
        # Meaning there has been a change (bounce) in between
        if res > RESIDUE_THRESHOLD:
            return BounceCalculator.calculate_bounce(history)
        return Ball()

    @staticmethod
    def calculate_bounce(history):
        # Since we have detected bounce AFTER it happened
        # To find coordinates, we have to go back one in history
        # Pass a parabola through those points and find coordinates
        last_balls_without_last = list(history)[-LEN_HISTORY_BOUNCE: -1]
        x_val = np.array([p.center[0] for p in last_balls_without_last])
        y_val = np.array([p.center[1] for p in last_balls_without_last])
        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                pol = np.polyfit(x_val, y_val, 2, full=False)  # We don't need quadratic residue
            except np.RankWarning:
                return Ball()

        # For minimizing the error, consider it as between last 2 points
        center_x = (history[-1].center[0] + history[-2].center[0]) / 2
        center_y = np.polyval(pol, center_x)

        bounce_ball = Ball((center_x, center_y))
        bounce_ball.is_bounce = True
        return bounce_ball
