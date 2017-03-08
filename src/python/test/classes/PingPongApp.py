# import the necessary packages

import cv2

from test.classes.BallTracker import BallTracker
from test.classes.utils.BallHistory import BallHistory
from test.classes.utils.Camera import Camera


class PingPongApp(object):
    def __init__(self, args):
        self.camera = Camera(args)

        self.writer = None
        if args.get("output", True):
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            height = self.camera.height
            width = self.camera.width
            self.writer = cv2.VideoWriter(args["output"], fourcc, args["frames"], (width, height), True)

        self.ballTracker = BallTracker(self.camera.height, self.camera.width)
        self.ballHistory = BallHistory(args["size"])
        self.loop = args["LOOP"]

    def run(self):
        while True:
            # grab the current frame
            frame = self.camera.get_next_frame(self.loop)
            if frame is None:
                if self.loop:
                    self.ballHistory.clear_history()
                    continue
                else:
                    break

            # Get next tracked center
            center = self.ballTracker.track(frame)
            if center:
                self.ballHistory.add_ball(center)

            # Paint calculated info
            self.paint_info(frame)

            # Write to file if necessary
            if self.writer is not None:
                self.writer.write(frame)

            if cv2.waitKey(1) & 0xFF is ord('q'):
                break

        # Clean up the camera and close any open windows
        self.camera.release()
        cv2.destroyAllWindows()

    def paint_info(self, frame):
        # loop over the set of tracked points
        if len(self.ballHistory) > 0:
            cv2.circle(frame, self.ballHistory[0].center, self.ballHistory[0].size, self.ballHistory[0].color, -1)
            for i in range(1, len(self.ballHistory)):
                prevBall, currBall = self.ballHistory[i - 1], self.ballHistory[i]
                # if either of the tracked points are None, ignore them
                if prevBall.center is None or currBall.center is None:
                    continue
                thickness = 3
                cv2.line(frame, prevBall.center, currBall.center, self.ballHistory.line_color(), thickness)
                cv2.circle(frame, currBall.center, currBall.size, currBall.color, -1)

        # show the frame to our screen
        cv2.imshow("Processed Frame", frame)
