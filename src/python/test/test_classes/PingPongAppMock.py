import cv2
import progressbar

from test.classes.PingPongApp import PingPongApp
from test.test_classes.BallHistoryMock import BallHistoryMock


class PingPongAppMock(PingPongApp):
    def __init__(self, args):
        super(PingPongAppMock, self).__init__(args)
        self.ballHistory = BallHistoryMock(args["size"])

    def run(self):
        print("Beginning test....")
        bar = progressbar.ProgressBar(max_value=self.camera.num_frames)

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
                self.ballHistory.add_ball(center, self.camera.get_curr_frame_number())

            if cv2.waitKey(1) & 0xFF is ord('q'):
                break

            bar.update(self.camera.get_curr_frame_number())

        # Clean up the camera and close any open windows
        self.ballHistory.end_test()
        self.camera.release()
        cv2.destroyAllWindows()
