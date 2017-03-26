# import the necessary packages

import cv2

from test.classes.game.Game import Game
from test.classes.utils.BallTracker import BallTracker
from test.classes.utils.Camera import Camera


class PingPongApp(object):
    def __init__(self, args):
        self.camera = Camera(args)

        height = self.camera.height
        width = self.camera.width

        self.writer = None
        if args.get("output", True):
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            self.writer = cv2.VideoWriter(args["output"], fourcc, args["frames"], (width, height), True)

        self.ballTracker = BallTracker(height, width)
        self.game = Game(args)
        self.loop = args["LOOP"]

    def run(self):
        while True:
            # grab the current frame
            frame = self.camera.get_next_frame(self.loop)
            if frame is None:
                if self.loop:
                    self.game.clear_history()
                    continue
                else:
                    break

            # Get next tracked center
            center = self.ballTracker.track(frame)
            self.game.update_history(center)

            # Paint calculated info
            processed_frame = self.paint_info(frame)

            # Show the frame to our screen
            cv2.imshow("Processed Frame", processed_frame)

            # Write to file if necessary
            if self.writer is not None:
                self.writer.write(processed_frame)

            if cv2.waitKey(1) & 0xFF is ord('q'):
                break

        # Clean up the camera and close any open windows
        self.camera.release()
        if self.writer:
            self.writer.release()
        cv2.destroyAllWindows()

    def paint_info(self, frame):
        # loop over the set of tracked points
        ball_history = self.game.ball_history
        if len(ball_history) > 0:
            cv2.circle(frame, ball_history[0].center, ball_history[0].size, ball_history[0].color, -1)
            for i in range(1, len(ball_history)):
                prevBall, currBall = ball_history[i - 1], ball_history[i]
                # if either of the tracked points are None, ignore them
                if prevBall.center is None or currBall.center is None:
                    continue
                thickness = 3
                cv2.line(frame, prevBall.center, currBall.center, ball_history.line_color(), thickness)
                cv2.circle(frame, currBall.center, currBall.size, currBall.color, -1)
        return frame
