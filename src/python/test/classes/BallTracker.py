# import the necessary packages

import time

import cv2

from test.classes.BallDetector import BallDetector
from test.classes.BallHistory import BallHistory
from test.classes.TableDetector import TableDetector


class BallTracker(object):
    def __init__(self, args):
        self.VIDEODEV = 0 if not args.get("video", False) else args["video"]

        self.camera = cv2.VideoCapture(self.VIDEODEV)
        assert self.camera.isOpened()

        if not args.get("output", False):
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            self.writer = cv2.VideoWriter(args["output"], fourcc, args["frames"],
                                          (int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                           int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))), True)
        
        self.ballHistory = BallHistory(args["size"])
        self.loop = args["LOOP"]

    def track(self):
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
                self.ballHistory.add_ball(center)

            # loop over the set of tracked points
            if len(self.ballHistory) > 0:
                cv2.circle(frame, self.ballHistory[0].center, 5, self.ballHistory[0].color, -1)
                for i in range(1, len(self.ballHistory)):
                    prevBall, currBall = self.ballHistory[i - 1], self.ballHistory[i]
                    # if either of the tracked points are None, ignore them
                    if prevBall.center is None or currBall.center is None:
                        continue
                    thickness = 3
                    cv2.line(frame, prevBall.center, currBall.center, self.ballHistory.line_color(), thickness)
                    cv2.circle(frame, currBall.center, 5, currBall.color, -1)

            # show the frame to our screen
            cv2.imshow("Frame", frame)
            if self.writer:
                self.writer.write(frame)
            cv2.imshow("Mask", maskBall)
            cv2.imshow("frameTable", frameTable)
            if cv2.waitKey(1) & 0xFF is ord('q'):
                break

        # cleanup the camera and close any open windows
        self.camera.release()
        cv2.destroyAllWindows()
