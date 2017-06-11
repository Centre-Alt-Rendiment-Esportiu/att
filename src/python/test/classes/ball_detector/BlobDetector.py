import cv2

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


class BlobDetector:
    def __init__(self):
        self.detector = cv2.SimpleBlobDetector_create(params)

    def detect_ball(self, frame):
        keypoints = self.detector.detect(frame)
        if keypoints:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Search for the whitest of all blobs
            whitest_point = max(keypoints, key=lambda x: hsv[int(x.pt[1])][int(x.pt[0])][2])
            return tuple([whitest_point.pt[0], whitest_point.pt[1]])
        return None
