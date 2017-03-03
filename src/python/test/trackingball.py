# import the necessary packages

from collections import deque
import numpy as np
import cv2
import time
import argparse

from test.classes.BallHistory import BallHistory


def tableDetector(frame):
    mask = cv2.inRange(frame, (131, 0, 255), (255, 255, 255))
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=5)
    mask = cv2.erode(mask, None, iterations=5)
    # mask = cv2.dilate(mask, None, iterations=5)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
        sort = sorted(cnts, key=cv2.contourArea, reverse=True)
        cmax = sort[1]
        epsilon = 0.1 * cv2.arcLength(cmax, True)
        approx = cv2.approxPolyDP(cmax, epsilon, True)
    return approx


ap = argparse.ArgumentParser()

ap.add_argument("-v", "--video",
                help="if present, path to the input video file")

ap.add_argument("-o", "--output",
                help="if present, path to the output video file")

ap.add_argument("-t", "--table",
                help="if present, table contour points")

ap.add_argument("-f", "--frames",
                help="if present, output video frames per second ", default=20)

ap.add_argument("-s", "--size",
                help="if present, ball tail size ", default=16)

ap.add_argument('-l', '--loop', dest='LOOP', action='store_true')
ap.add_argument('--no-loop', dest='LOOP', action='store_false')
ap.set_defaults(LOOP=False)

args = vars(ap.parse_args())

if not args.get("video", False):
    VIDEODEV = 0
else:
    VIDEODEV = args["video"]

if not args.get("output", False):
    OUTPUT = False
else:
    OUTPUT = args["output"]
LOOP = args["LOOP"]

camera = cv2.VideoCapture(VIDEODEV);
assert camera.isOpened()

colorLower = (154, 0, 255)
colorUpper = (255, 255, 255)
width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
tailsize = args["size"]
ballHistory = BallHistory(tailsize)

if not args["table"]:
    table = True
else:
    table = False
    tableContours = np.load(args["table"])
    maskTable = np.zeros((height, width), np.uint8)
    # 0 is table, 1 is background
    cv2.fillConvexPoly(maskTable, tableContours, 1)
    maskTable = np.dstack(3 * (maskTable,))

if OUTPUT:
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    writer = cv2.VideoWriter(OUTPUT, fourcc, args["frames"], (int(width), int(height)), True)

while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    if not grabbed:
        if LOOP:
            camera.set(cv2.CAP_PROP_FRAME_COUNT, 0)
            camera.release()
            camera = cv2.VideoCapture(VIDEODEV)
            ballHistory.clear_history()
            time.sleep(0.02)
            continue
        else:
            break

    # first frame detect table

    if table:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        tableContours = tableDetector(hsv)
        maskTable = np.zeros((height, width), np.uint8)
        # 0 is table, 1 is background
        cv2.fillConvexPoly(maskTable, tableContours, 1)
        maskTable = np.dstack(3 * (maskTable,))
        table = False

    # add maskTable to frame
    frameTable = frame * maskTable
    hsv = cv2.cvtColor(frameTable, cv2.COLOR_BGR2HSV)

    # find white color mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)

    mask = cv2.dilate(mask, None, iterations=2)
    # mask= cv2.erode(mask, None, iterations=1)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    # only proceed if at least one contour was found
    reset = True
    # TODO search by shape the ball
    if len(cnts) > 0:
        cmax = max(cnts, key=cv2.contourArea)
        # if cv2.contourArea(cmax)>20 :
        # print cv2.contourArea(cmax)
        M = cv2.moments(cmax)
        if M["m00"] > 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # cv2.circle(frame, center, 5, (0, 255, 0), -1)
            # calculate direction of ball, paint it if change clear
            ballHistory.add_ball(center)
    # loop over the set of tracked points
    if len(ballHistory) > 0:
        cv2.circle(frame, ballHistory[0].center, 5, ballHistory[0].color, -1)
        for i in range(1, len(ballHistory)):
            prevBall, currBall = ballHistory[i - 1], ballHistory[i]
            # if either of the tracked points are None, ignore them
            if prevBall.center is None or currBall.center is None:
                continue
            thickness = 3
            cv2.line(frame, prevBall.center, currBall.center, ballHistory.line_color(), thickness)
            cv2.circle(frame, currBall.center, 5, prevBall.color, -1)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    if OUTPUT:
        writer.write(frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("frameTable", frameTable)
    if cv2.waitKey(1) & 0xFF is ord('q'):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
