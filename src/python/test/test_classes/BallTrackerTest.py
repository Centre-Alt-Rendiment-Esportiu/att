import cv2
import time

import progressbar

from test.classes.BallDetector import BallDetector
from test.classes.TableDetector import TableDetector
from test.classes.BallTracker import BallTracker
from test.test_classes.BallHistoryTest import BallHistoryTest


class BallTrackerTest(BallTracker):
    def __init__(self, args):
        super(BallTrackerTest, self).__init__(args)
        self.ballHistory = BallHistoryTest(args["size"])

    def track(self):
        print("Beginning test....")

        max_frames = int(self.camera.get(cv2.CAP_PROP_FRAME_COUNT))
        bar = progressbar.ProgressBar(max_value=max_frames)

        firstFrame = True
        while True:
            # grab the current frame
            (grabbed, frame) = self.camera.read()

            if not grabbed:
                if self.loop:
                    self.camera.set(cv2.CAP_PROP_FRAME_COUNT, 0)
                    self.camera.release()
                    self.camera = cv2.VideoCapture(self.VIDEODEV)
                    self.ballHistory.clear_history()
                    time.sleep(0.02)
                    continue
                else:
                    break

            curr_frame = int(self.camera.get(cv2.CAP_PROP_POS_FRAMES))
            bar.update(curr_frame)

            # first frame detect table
            if firstFrame:
                tableContours = TableDetector.detect(frame)
                maskTable = TableDetector.create_table_mask(tableContours,
                                                            int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                                            int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)))
                firstFrame = False

            # add maskTable to frame
            frameTable = frame * maskTable


            maskBall = BallDetector.create_ball_mask(frameTable)
            center = BallDetector.detect(maskBall)
            if center:
                self.ballHistory.add_ball(center, curr_frame)

            if cv2.waitKey(1) & 0xFF is ord('q'):
                break

        # cleanup the camera and close any open windows
        self.ballHistory.end_test()
        self.camera.release()
        cv2.destroyAllWindows()
