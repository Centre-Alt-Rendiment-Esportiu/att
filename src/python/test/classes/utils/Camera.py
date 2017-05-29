import time

import cv2

from test.classes.utils.CameraCalibrate import CameraCalibrate


class Camera:
    def __init__(self, args):
        self.VIDEODEV = 0 if not args.get("video", False) else args["video"]
        self.camera = cv2.VideoCapture(self.VIDEODEV)
        assert self.camera.isOpened()
        self.height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.num_frames = int(self.camera.get(cv2.CAP_PROP_FRAME_COUNT))
        self.loop = args["LOOP"]

        self.calibrator = CameraCalibrate()

    def get_next_frame(self):
        (grabbed, frame) = self.camera.read()

        if not grabbed:
            if self.loop:
                self.camera.set(cv2.CAP_PROP_FRAME_COUNT, 0)
                self.camera.release()
                self.camera = cv2.VideoCapture(self.VIDEODEV)
                time.sleep(0.02)
            return None

        undistorted_frame = self.calibrator.undistort(frame)
        return undistorted_frame

    def get_curr_frame_number(self):
        return int(self.camera.get(cv2.CAP_PROP_POS_FRAMES))

    def release(self):
        self.camera.release()
