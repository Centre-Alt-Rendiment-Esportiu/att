import cv2
import numpy as np

sensitivity = 15
lower_white = np.array([0, 0, 255-sensitivity])
upper_white = np.array([255, sensitivity, 255])


class BallDetector:
    @staticmethod
    def detect(frame):
        mask = BallDetector.create_ball_mask(frame)
        # gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        gray_mask = mask
        cnts = cv2.findContours(gray_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            cmax = max(cnts, key=cv2.contourArea)
            M = cv2.moments(cmax)
            if M["m00"] > 0:
                center = (int(np.rint(M["m10"] / M["m00"])), int(np.rint(M["m01"] / M["m00"])))
        return center

    @staticmethod
    def create_ball_mask(frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # find white color maskBall
        # mask = cv2.dilate(hsv, None, iterations=0)
        morph = cv2.morphologyEx(hsv, cv2.MORPH_CLOSE, (10, 10))
        mask = cv2.inRange(morph, lower_white, upper_white)
        return mask
