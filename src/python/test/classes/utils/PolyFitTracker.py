from collections import deque

import numpy as np

from test.classes.utils.Ball import Ball


class PolyFitTracker:
    def __init__(self):
        self.max_history = 8
        self.ball_queue = deque()

    def add_ball(self, point):
        self.ball_queue.append(point)

    def extrapolate(self):
        real_balls = list(filter(lambda x: not x.is_extrapolate, self.ball_queue))
        if len(real_balls) < 5:
            return

        # Don't extrapolate if it's very far away from x_bound in terms of max_length
        max_length = abs(real_balls[0].center[0] - real_balls[-1].center[0])
        x_bound = real_balls[-1].center[0]

        b1, b2 = self.ball_queue[-1], self.ball_queue[-2]
        x1, x2 = b1.center[0], b2.center[0]

        extrapol_x = 2 * x1 - x2  # x1 + (x1 - x2)
        if abs(extrapol_x - x_bound) > max_length / 2:
            return

        # Evaluate parabola at next possible point
        x_val = np.array([p.center[0] for p in real_balls])
        y_val = np.array([p.center[1] for p in real_balls])
        pol = np.polyfit(x_val, y_val, 2, full=False)

        extrapol_y = int(np.rint(np.polyval(pol, extrapol_x)))

        extrapol_ball = Ball(tuple([extrapol_x, extrapol_y]))
        extrapol_ball.is_extrapolate = True
        return extrapol_ball

    def find_bounce(self):
        if len(self.ball_queue) < 3:
            return
        last_balls = list(self.ball_queue)[-self.max_history:]
        x_val = np.array([p.center[0] for p in last_balls])
        y_val = np.array([p.center[1] for p in last_balls])
        _pol, res, _rank, _sing, _rcond = np.polyfit(x_val, y_val, 2, full=True)

        if res > 7:
            last_balls_without_last = list(self.ball_queue)[-self.max_history+1:-1]
            x_val = np.array([p.center[0] for p in last_balls_without_last])
            y_val = np.array([p.center[1] for p in last_balls_without_last])
            pol = np.polyfit(x_val, y_val, 2, full=False)  # We don't need quadratic residue

            center_x = int(np.rint(self.ball_queue[-1].center[0] + self.ball_queue[-2].center[0]) / 2)
            center_y = int(np.rint(np.polyval(pol, center_x)))

            last_point = self.ball_queue[-1]
            self.clear()
            self.add_ball(last_point)

            bounce_ball = Ball(tuple([center_x, center_y]))
            bounce_ball.is_bounce = True
            return bounce_ball
        return None

    def find_bounce2(self):
        if len(self.ball_queue) < 3:
            return

        last_balls_without_last = list(self.ball_queue)[-self.max_history + 1:-1]
        x_val = np.array([p.center[0] for p in last_balls_without_last])
        y_val = np.array([p.center[1] for p in last_balls_without_last])
        pol = np.polyfit(x_val, y_val, 2, full=False)

        x1, y1 = self.ball_queue[-1].center
        x2 = self.ball_queue[-2].center[0]
        y2 = int(np.rint(np.polyval(pol, x1)))

        if abs(y1-y2) > 0.3 * abs(x1-x2):
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
        self.ball_queue.clear()
