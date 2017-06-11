import warnings

import numpy as np

from test.classes.utils.Ball import Ball

LEN_EXTRAPOL = 4


class Extrapolator:
    def extrapolate(self, history):
        real_balls = list(filter(lambda x: not x.is_extrapolate, history))
        # Don't extrapolate if there aren't enough balls to do so
        if len(real_balls) < LEN_EXTRAPOL:
            return Ball()

        # Do not extrapolate more than once in a row
        if history[-1].is_extrapolate:
            return Ball()

        # Fit parabola on all real_balls
        x_val = np.array([p.center[0] for p in real_balls[-LEN_EXTRAPOL:]])
        y_val = np.array([p.center[1] for p in real_balls[-LEN_EXTRAPOL:]])

        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                pol = np.polyfit(x_val, y_val, 2, full=False)
            except np.RankWarning:
                return Ball()

        # We grab last 2 balls let them be extrapolates or not
        b1, b2 = history[-1], history[-2]
        x1, x2 = b1.center[0], b2.center[0]

        # Predicted value is at x = x1 + (x1-x2) = 2*x1 - x2
        extrapol_x = 2 * x1 - x2
        # Evaluate parabola at x = 2*x1 - x2
        extrapol_y = np.polyval(pol, extrapol_x)

        extrapol_ball = Ball((extrapol_x, extrapol_y))
        extrapol_ball.is_extrapolate = True
        return extrapol_ball
