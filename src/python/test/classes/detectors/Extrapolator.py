import numpy as np

from test.classes.utils.Ball import Ball
from test.classes.utils.BallHistory import BallHistory

MIN_HISTORY_EXTRAPOL = 5


class Extrapolator:
    def __init__(self):
        self.ball_queue = BallHistory()

    def add_ball(self, ball):
        self.ball_queue.update_history(ball)

    def extrapolate(self):
        real_balls = list(filter(lambda x: not x.is_extrapolate, self.ball_queue))
        # Don't extrapolate if there aren't enough balls to do so
        if len(real_balls) < MIN_HISTORY_EXTRAPOL:
            return None

        max_length = abs(real_balls[0].center[0] - real_balls[-1].center[0])
        x_bound = real_balls[-1].center[0]

        b1, b2 = self.ball_queue[-1], self.ball_queue[-2]
        x1, x2 = b1.center[0], b2.center[0]

        # Predicted value is at x = x1 + (x1-x2) = 2*x1 - x2
        extrapol_x = 2 * x1 - x2

        # Don't extrapolate if it's very far away from x_bound in terms of max_length
        if abs(extrapol_x - x_bound) > max_length / 3:
            return None

        # Pass parabola through all real_balls
        x_val = np.array([p.center[0] for p in real_balls])
        y_val = np.array([p.center[1] for p in real_balls])
        pol = np.polyfit(x_val, y_val, 2, full=False)

        # Evaluate parabola at x = 2*x1 - x2
        extrapol_y = np.polyval(pol, extrapol_x)

        extrapol_ball = Ball(tuple([extrapol_x, extrapol_y]))
        extrapol_ball.is_extrapolate = True
        return extrapol_ball

    def clear(self):
        self.ball_queue.clear_history()
