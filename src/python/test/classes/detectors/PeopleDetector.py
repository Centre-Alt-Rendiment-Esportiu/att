import cv2


class PeopleDetector:
    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        # self.hog.winsize = (48, 96)
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def detect(self, frame):
        winStride = (8, 8)
        padding = (32, 32)
        scale = 1.05

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        (rects, weights) = self.hog.detectMultiScale(gray_frame,
                                                     winStride=winStride,
                                                     padding=padding,
                                                     scale=scale)

        for (x, y, w, h) in rects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 255), 2)

        cv2.imshow('Image', frame)
