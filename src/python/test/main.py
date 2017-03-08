import argparse

from test.classes.PingPongApp import PingPongApp
from test.test_classes.PingPongAppMock import PingPongAppMock

ap = argparse.ArgumentParser()

ap.add_argument("-v", "--video",
                help="if present, path to the input video file")

ap.add_argument("-o", "--output",
                help="if present, path to the output video file")

# Should detect table, not enter it
# ap.add_argument("-t", "--table",
#               help="if present, table contour points")

ap.add_argument("-f", "--frames",
                help="if present, output video frames per second ", default=20)

ap.add_argument("-s", "--size",
                help="if present, ball tail size ", default=16)

ap.add_argument('-l', '--loop', dest='LOOP', action='store_true')
ap.add_argument('--no-loop', dest='LOOP', action='store_false')
ap.set_defaults(LOOP=False)

ap.add_argument("-t", "--test", dest="TEST", action='store_true')
ap.set_defaults(TEST=False)

args = vars(ap.parse_args())

if args["TEST"]:
    ping_pong_app = PingPongAppMock(args)
else:
    ping_pong_app = PingPongApp(args)
ping_pong_app.run()
