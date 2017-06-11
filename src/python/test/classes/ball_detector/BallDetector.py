from collections import deque

import cv2
import numpy as np

from test.classes.ball_detector.BackgroundDetector import BackgroundDetector
from test.classes.ball_detector.BlobDetector import BlobDetector
from test.classes.ball_detector.Neighborhood import Neighborhood
from test.classes.ball_detector.TableDetector import TableDetector
from test.classes.utils.Ball import Ball
from test.classes.utils.BallState import PositionState

sensitivity = 15
lower_white = np.array([0, 0, 255 - sensitivity])
upper_white = np.array([255, sensitivity, 255])


class BallDetector:
    def __init__(self, first_frame):
        # We only search the ball if it's not on the white line
        # We do that by removing all white pixels on initial image - dilation just in case
        # It would be extrapolated anyways and adds error to detection otherwise
        frame_hsv = cv2.cvtColor(first_frame, cv2.COLOR_BGR2HSV)
        white_mask = cv2.inRange(frame_hsv, lower_white, upper_white)
        white_mask = cv2.dilate(white_mask, np.ones((3, 3), np.uint8), iterations=1)
        self.non_white_mask = 255 - white_mask

        self.table = TableDetector(white_mask)

        self.background = BackgroundDetector()
        self.blobs = BlobDetector()
        self.prevs = deque(maxlen=2)
        self.clear()

    def detect(self, fr):
        # Filter out white pixels
        frame = cv2.bitwise_and(fr, fr, mask=self.non_white_mask)
        # Update background subtractor
        self.background.update(frame)

        # CREATE NEIGHBORHOOD FRAME
        # Circle centered in prev1, with radius 2 * norm(prev2-prev1)
        # if prev1 and prev2 exist, otherwise it leaves frame as it is

        neighborhood = Neighborhood(self.prevs[-1], self.prevs[-2], factor=2)
        frame_neighborhood = neighborhood.apply(frame)

        # SEARCH INSIDE TABLE

        frame_in_table = self.table.apply_inside(frame_neighborhood)
        center = self.inside_detect(frame_in_table)
        if center:
            detected_ball = Ball(center)
            detected_ball.position_state = PositionState.IN
            self.update_prev(detected_ball)
            return detected_ball

        # If not found inside table,
        # SEARCH OUTSIDE TABLE

        frame_out_table = self.table.apply_outside(frame_neighborhood)
        background_sub = self.background.apply(frame_out_table)

        center = self.outside_detect(background_sub)
        if center:
            detected_ball = Ball(center)
            detected_ball.position_state = PositionState.OUT
            self.update_prev(detected_ball)
            return detected_ball

        self.update_prev(Ball())
        # Not found anywhere: return None
        return Ball()

    def update_prev(self, prev):
        self.prevs.append(prev)

    def clear(self):
        self.prevs.append(Ball())
        self.prevs.append(Ball())

    def is_inside_table(self, ball):
        return self.table.is_inside(ball.center)

    def inside_detect(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_white, upper_white)
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        center = None
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            cmax = max(cnts, key=cv2.contourArea)
            M = cv2.moments(cmax)
            if M["m00"] > 0:
                center = (M["m10"] / M["m00"], M["m01"] / M["m00"])
        return center

    def outside_detect(self, frame):
        return self.blobs.detect_ball(frame)
