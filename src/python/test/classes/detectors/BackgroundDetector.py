import cv2


class BackgroundDetector:
    def __init__(self):
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=15, varThreshold=9, detectShadows=False)
        self.background_filter = None

    def update(self, frame):
        self.background_filter = self.fgbg.apply(frame)

    def detect(self, frame):
        # Remove salt and pepper noise
        median_filter = cv2.medianBlur(self.background_filter, 5)
        # Apply background subtracted frame
        extracted_frame = cv2.bitwise_and(frame, frame, mask=median_filter)

        return extracted_frame
