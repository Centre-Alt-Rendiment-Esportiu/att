from collections import deque
import numpy as np
from scipy.interpolate import BSpline, splrep, UnivariateSpline

from test.classes.utils.Ball import Ball


class PolyFitTracker:
    def __init__(self):
        self.pol = None
        self.res = 0
        self.ball_queue = deque()

    def add_point(self, point):
        self.ball_queue.append(point)
        self.update()

    def update(self):
        real_balls = list(filter(lambda x: not x.is_extrapolate, self.ball_queue))
        if len(real_balls) < 3:
            return
        x_val = np.array([p.center[0] for p in real_balls])
        y_val = np.array([p.center[1] for p in real_balls])
        self.pol, self.res, rank, sing, rcond = np.polyfit(x_val, y_val, 2, full=True)

    def extrapolate(self):
        if self.pol is None:
            return

        b1, b2 = self.ball_queue[-1], self.ball_queue[-2]

        x1, x2 = b1.center[0], b2.center[0]

        extrapol_x = 2 * x1 - x2
        extrapol_y = int(np.rint(np.polyval(self.pol, extrapol_x)))

        return Ball(tuple([extrapol_x, extrapol_y]))

    def find_bounce(self):
        if self.pol is None:
            return

        if self.res > 7:
            center_x = int(np.rint(self.ball_queue[-1].center[0] + self.ball_queue[-2].center[0]) / 2)
            center_y = int(np.rint(np.polyval(self.pol, center_x)))
            last_point = self.ball_queue[-1]
            self.clear()
            self.add_point(last_point)
            return Ball(tuple([center_x, center_y]))
            # real_balls = list(filter(lambda x: not x.is_extrapolate, self.ball_queue))
            #
            # x_val = np.array([x.center[0] for x in real_balls])
            # y_val = np.array([x.center[1] for x in real_balls])
            # order = np.argsort(x_val)
            #
            # spline = UnivariateSpline(x=x_val[order], y=y_val[order], k=2)
            # crit_pts = spline.derivative().roots()
            # bounce_point = min(crit_pts, key=lambda x: abs(x - self.ball_queue[-1].center[0]))
            #
            # knots = spline.get_knots()
            # coeffs = spline.get_coeffs()
            # bs_spline = BSpline(knots, coeffs, 2)
            #
            # last_point = self.ball_queue[-1]
            # self.clear()
            # self.add_point(last_point)
            # return bounce_point

    def clear(self):
        self.pol = None
        self.res = 0
        self.ball_queue.clear()
