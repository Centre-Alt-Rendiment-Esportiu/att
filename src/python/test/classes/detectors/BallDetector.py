from collections import deque

import cv2
import numpy as np

from test.classes.detectors.BackgroundDetector import BackgroundDetector
from test.classes.detectors.TableDetector import TableDetector
from test.classes.utils.Ball import Ball
from test.classes.utils.BallState import PositionState
from test.classes.utils.Neighborhood import Neighborhood

sensitivity = 15
lower_white = np.array([0, 0, 255 - sensitivity])
upper_white = np.array([255, sensitivity, 255])

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
# params.minThreshold = 10
# params.maxThreshold = 200

params.filterByColor = True
params.blobColor = 255

# Filter by Area.
params.filterByArea = True
params.minArea = 100
# params.maxArea = 2000

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.75

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.9

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.08

detector = cv2.SimpleBlobDetector_create(params)


class BallDetector:
    def __init__(self, first_frame):
        self.table = TableDetector(first_frame)
        self.background = BackgroundDetector()
        self.prevs = deque(maxlen=2)
        self.prevs.append(None)
        self.prevs.append(None)

    def detect(self, frame):
        # Update background subtractor
        self.background.update(frame)

        # CREATE NEIGHBORHOOD FRAME
        # Circle centered in prev1, with radius 2 * norm(prev2-prev1)
        # if prev1 and prev2 exist, otherwise it leaves frame as it is

        neighborhood = Neighborhood(self.prevs[-1], self.prevs[-2], factor=2)
        frame_neighborhood = neighborhood.apply(frame)

        # SEARCH INSIDE TABLE

        frame_in_table = self.table.apply(frame_neighborhood)
        center = BallDetector.inside_detect(frame_in_table)
        if center:
            detected_ball = Ball(center)
            detected_ball.position_state = PositionState.IN
            self.update_prev(detected_ball)
            return detected_ball

        # If not found inside table,
        # SEARCH OUTSIDE TABLE

        frame_out_table = frame_neighborhood
        background_sub = self.background.apply(frame_out_table)

        center = BallDetector.outside_detect(background_sub)
        if center:
            detected_ball = Ball(center)
            detected_ball.position_state = PositionState.OUT
            self.update_prev(detected_ball)
            return detected_ball

        self.update_prev(None)
        # Not found anywhere: return None
        return None

    def update_prev(self, prev):
        self.prevs.append(prev)

    @staticmethod
    def inside_detect(frame):
        mask = BallDetector.create_ball_mask(frame)
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            cmax = max(cnts, key=cv2.contourArea)
            M = cv2.moments(cmax)
            if M["m00"] > 0:
                center = (M["m10"] / M["m00"], M["m01"] / M["m00"])
        return center

    @staticmethod
    def outside_detect(frame):
        keypoints = detector.detect(frame)
        if keypoints:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Search for the whitest of all blobs
            whitest_point = max(keypoints, key=lambda x: hsv[int(x.pt[1])][int(x.pt[0])][2])
            return tuple([whitest_point.pt[0], whitest_point.pt[1]])
        return None

    @staticmethod
    def create_ball_mask(frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_white, upper_white)
        return mask
