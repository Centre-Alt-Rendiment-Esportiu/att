import cv2
from numpy import rint

min_color = (154, 0, 255)
max_color = (255, 255, 255)


class BallDetector:
    @staticmethod
    def detect(frame):
        mask = BallDetector.create_ball_mask(frame)
        gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        cnts = cv2.findContours(gray_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            cmax = max(cnts, key=cv2.contourArea)
            M = cv2.moments(cmax)
            if M["m00"] > 0:
                center = (int(rint(M["m10"] / M["m00"])), int(rint(M["m01"] / M["m00"])))
        return center

    @staticmethod
    def create_ball_mask(frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # find white color maskBall
        mask = cv2.inRange(hsv, min_color, max_color)
        #mask = cv2.dilate(hsv, None, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, (20, 20))
        return frame
