import cv2

from test.classes.utils.BallHistory import BallHistory

MAX_FRAMES_SINCE_BALL = 5


class PaintHistory:
    def __init__(self):
        self.ball_history = BallHistory(tail_size=16)
        self.frames_since_ball = 0

    def update_history(self, ball):
        if not ball.is_none():
            # NOTE Cannot paint floats!
            ball.center = (int(ball.center[0]), int(ball.center[1]))
            self.ball_history.update_history(ball)
            self.frames_since_ball = 0
        else:
            # If too much time has passed since we last had balls, just delete everything
            if self.frames_since_ball > MAX_FRAMES_SINCE_BALL:
                self.clear()
            else:
                self.frames_since_ball += 1

    def draw_info(self, frame):
        b_h = self.ball_history
        if len(b_h) > 0:
            cv2.circle(frame, b_h[0].center, b_h[0].get_size(), b_h[0].get_color(), -1)
            for i in range(1, len(b_h)):
                prev_b, curr_b = b_h[i - 1], b_h[i]
                thickness = 3
                cv2.line(frame, prev_b.center, curr_b.center, b_h.line_color(), thickness)
                cv2.circle(frame, curr_b.center, curr_b.get_size(), curr_b.get_color(), -1)
        return frame

    def clear(self):
        self.ball_history.clear_history()
