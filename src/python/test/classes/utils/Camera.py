import time
import cv2


class Camera:
    def __init__(self, args):
        self.VIDEODEV = 0 if not args.get("video", False) else args["video"]
        self.camera = cv2.VideoCapture(self.VIDEODEV)
        assert self.camera.isOpened()
        self.height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.num_frames = int(self.camera.get(cv2.CAP_PROP_FRAME_COUNT))

    def get_next_frame(self, loop=False):
        (grabbed, frame) = self.camera.read()

        if not grabbed:
            if loop:
                self.camera.set(cv2.CAP_PROP_FRAME_COUNT, 0)
                self.camera.release()
                self.camera = cv2.VideoCapture(self.VIDEODEV)
                time.sleep(0.02)
            return None

        return frame

    def get_curr_frame_number(self):
        return int(self.camera.get(cv2.CAP_PROP_POS_FRAMES))

    def release(self):
        self.camera.release()
