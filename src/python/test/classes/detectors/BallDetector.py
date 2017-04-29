import cv2
import numpy as np

sensitivity = 15
lower_white = np.array([0, 0, 255-sensitivity])
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
    @staticmethod
    def create_ball_mask(frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_white, upper_white)
        return mask

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
                center = (int(np.rint(M["m10"] / M["m00"])), int(np.rint(M["m01"] / M["m00"])))
        return center

    @staticmethod
    def outside_detect(frame):
        keypoints = detector.detect(frame)
        if keypoints:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Search for the whitest of all blobs
            whitest_point = max(keypoints, key=lambda x: hsv[int(x.pt[1])][int(x.pt[0])][2])
            return tuple([int(whitest_point.pt[0]), int(whitest_point.pt[1])])
        return None
