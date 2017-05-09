import numpy as np

from test.classes.utils.Ball import Ball
from test.classes.utils.BallHistory import BallHistory

MIN_HISTORY_EXTRAPOL = 5


class Extrapolator:
    @staticmethod
    def extrapolate(history):
        real_balls = list(filter(lambda x: not x.is_extrapolate, history))
        # Don't extrapolate if there aren't enough balls to do so
        if len(real_balls) < MIN_HISTORY_EXTRAPOL:
            return Ball()

        # Do not extrapolate more than twice in a row
        if history[-1].is_extrapolate and history[-2].is_extrapolate:
            return Ball()

        max_length = abs(real_balls[0].center[0] - real_balls[-1].center[0])
        x_bound = real_balls[-1].center[0]

        b1, b2 = history[-1], history[-2]
        x1, x2 = b1.center[0], b2.center[0]

        # Predicted value is at x = x1 + (x1-x2) = 2*x1 - x2
        extrapol_x = 2 * x1 - x2

        # Don't extrapolate if it's very far away from x_bound in terms of max_length
        if abs(extrapol_x - x_bound) > max_length / 2:
            return Ball()

        # Pass parabola through all real_balls
        x_val = np.array([p.center[0] for p in real_balls])
        y_val = np.array([p.center[1] for p in real_balls])
        pol = np.polyfit(x_val, y_val, 2, full=False)

        # Evaluate parabola at x = 2*x1 - x2
        extrapol_y = np.polyval(pol, extrapol_x)

        extrapol_ball = Ball((extrapol_x, extrapol_y))
        extrapol_ball.is_extrapolate = True
        return extrapol_ball
