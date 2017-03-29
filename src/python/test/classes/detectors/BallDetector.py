import cv2
import numpy as np

sensitivity = 15
lower_white = np.array([0, 0, 255-sensitivity])
upper_white = np.array([255, sensitivity, 255])


class BallDetector:
    @staticmethod
    def create_ball_mask(frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # find white color maskBall
        # mask = cv2.dilate(hsv, None, iterations=0)
        morph = cv2.morphologyEx(hsv, cv2.MORPH_CLOSE, (10, 10))
        mask = cv2.inRange(morph, lower_white, upper_white)
        return mask


    @staticmethod
    def simple_detect(frame):
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
    def complex_detect(frame):
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
        params.minConvexity = 0.87

        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.05

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(frame)

        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # Show keypoints
        cv2.imshow("Keypoints", im_with_keypoints)

        if keypoints:
            key = keypoints[0].pt
            tmp = frame[int(key[1])][int(key[0])]
            whitest_point = max(keypoints, key=lambda x: int(frame[int(x.pt[1])][int(x.pt[0])][0]) +
                                                         int(frame[int(x.pt[1])][int(x.pt[0])][1]) +
                                                         int(frame[int(x.pt[1])][int(x.pt[0])][2])
                                )

            return tuple([int(whitest_point.pt[0]), int(whitest_point.pt[1])])
        return None