import cv2

from test.classes.detectors.BallDetector import BallDetector
from test.classes.game.BallHistory import BallHistory
from test.classes.utils.BallState import PositionState
from test.classes.utils.PolyFitTracker import PolyFitTracker


class BallTracker(object):
    def __init__(self):
        self.polyfit_tracker = PolyFitTracker()
        self.ball_history = BallHistory()
        self.ball_detector = None

    def first_frame(self, first_frame):
        self.ball_detector = BallDetector(first_frame)

    def track(self, frame):
        detected_ball = self.ball_detector.detect(frame)
        if detected_ball is not None:
            if self.ball_history.check_direction_change(detected_ball):
                self.polyfit_tracker.clear()

            self.polyfit_tracker.add_ball(detected_ball)

            bounce = self.polyfit_tracker.find_bounce()
            if bounce is not None:
                bounce.position_state = PositionState.IN \
                    if self.ball_detector.is_inside_table(bounce.center) \
                    else PositionState.OUT
                self.ball_history.update_history(bounce)

            self.ball_history.update_history(detected_ball)

        else:
            extrapol_ball = self.polyfit_tracker.extrapolate()
            if extrapol_ball is not None:
                # self.polyfit_tracker.add_ball(extrapol_ball)
                self.ball_detector.update_prev(extrapol_ball.center)

                bounce = self.polyfit_tracker.find_bounce()
                if bounce is not None:
                    bounce.position_state = PositionState.IN \
                        if self.ball_detector.is_inside_table(bounce.center) \
                        else PositionState.OUT
                    self.ball_history.update_history(bounce)

                self.ball_history.update_history(extrapol_ball)

        tracked_frame = self.paint_info(frame)
        return tracked_frame

    def clear_history(self):
        self.ball_history.clear_history()

    def paint_info(self, frame):
        # TODO : Paint scoreboard
        # text = 'Points: ' + str(self.game.players[0].score) + ' - ' + str(self.game.players[1].score)
        # cv2.putText(frame, text, (10, 500), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)

        # loop over the set of tracked points
        # And paint them on the frame
        b_h = self.ball_history
        if len(b_h) > 0:
            cv2.circle(frame, b_h[0].center, b_h[0].get_size(), b_h[0].get_color(), -1)
            for i in range(1, len(b_h)):
                prev_b, curr_b = b_h[i - 1], b_h[i]
                # if either of the tracked balls are None, ignore them
                if prev_b.center is None or curr_b.center is None:
                    continue
                thickness = 3
                cv2.line(frame, prev_b.center, curr_b.center, b_h.line_color(), thickness)
                cv2.circle(frame, curr_b.center, curr_b.get_size(), curr_b.get_color(), -1)
        return frame