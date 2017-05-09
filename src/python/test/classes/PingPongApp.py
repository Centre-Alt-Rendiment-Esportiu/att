# import the necessary packages

import cv2
import progressbar

from test.classes.utils.BallTracker import BallTracker
from test.classes.utils.Camera import Camera
from test.classes.utils.PaintHistory import PaintHistory


class PingPongApp(object):
    def __init__(self, args):
        self.camera = Camera(args)

        self.writer = None
        if args.get("output", True):
            height = self.camera.height
            width = self.camera.width
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            self.writer = cv2.VideoWriter(args["output"], fourcc, args["frames"], (width, height), True)

        self.ball_tracker = BallTracker()
        self.paint_history = PaintHistory()
        self.loop = args["LOOP"]

    def run(self):
        first_frame = True

        print("Processing video....")
        bar = progressbar.ProgressBar(max_value=self.camera.num_frames)

        while True:
            # grab the current frame
            frame = self.camera.get_next_frame()
            if frame is None:
                if self.loop:
                    self.paint_history.clear()
                    self.ball_tracker.clear()
                    continue
                else:
                    break

            if first_frame:
                self.ball_tracker.first_frame(frame)
                first_frame = False
                continue

            found_ball = self.ball_tracker.track(frame)
            bounce_ball = self.ball_tracker.get_bounce()

            # Reversed order because bounce is previous to found
            self.paint_history.update_history(bounce_ball)
            self.paint_history.update_history(found_ball)

            tracked_frame = self.paint_history.draw_info(frame)
            # Write to file if asked
            if self.writer is not None:
                self.writer.write(tracked_frame)
                bar.update(self.camera.get_curr_frame_number())
            # If not, show on screen
            else:
                cv2.imshow("PingPongApp", tracked_frame)

            if cv2.waitKey(1) & 0xFF is ord('q'):
                break

        # Clean up the camera and close any open windows
        self.camera.release()
        if self.writer:
            self.writer.release()
        cv2.destroyAllWindows()
