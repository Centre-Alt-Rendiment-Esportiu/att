import cv2


class BackgroundDetector:
    def __init__(self):
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=15, varThreshold=9, detectShadows=False)
        self.background_filter = None

    def update(self, frame):
        self.background_filter = self.fgbg.apply(frame)

    def detect(self, frame):
        # Remove salt and pepper noise
        # median_filter = cv2.medianBlur(self.background_filter, 5)
        # Apply background subtracted frame
        median_filter = cv2.medianBlur(self.background_filter, 5)
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        final_filter = cv2.morphologyEx(median_filter, cv2.MORPH_CLOSE, (2, 2))

        extracted_frame = cv2.bitwise_and(frame, frame, mask=final_filter)

        return extracted_frame
