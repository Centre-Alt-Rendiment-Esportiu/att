import cv2

min_color = (154, 0, 255)
max_color = (255, 255, 255)


class BallDetector:
    @staticmethod
    def create_ball_mask(frameTable):
        hsv = cv2.cvtColor(frameTable, cv2.COLOR_BGR2HSV)
        # find white color maskBall
        mask = cv2.inRange(hsv, min_color, max_color)
        mask = cv2.dilate(mask, None, iterations=2)
        # maskBall= cv2.erode(maskBall, None, iterations=1)
        return mask

    @staticmethod
    def detect(mask):
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        # only proceed if at least one contour was found
        # TODO search by shape the ball
        if len(cnts) > 0:
            cmax = max(cnts, key=cv2.contourArea)
            M = cv2.moments(cmax)
            if M["m00"] > 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        return center
