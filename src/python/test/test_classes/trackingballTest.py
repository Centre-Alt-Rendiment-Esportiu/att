# import the necessary packages

import argparse

import cv2
import numpy as np

from test.test_classes.BallHistoryTest import BallHistoryTest


def table_detector(frame):
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

args = vars(ap.parse_args())

if not args.get("video", False):
    VIDEODEV = 0
else:
    VIDEODEV = args["video"]

camera = cv2.VideoCapture(VIDEODEV)
assert camera.isOpened()

colorLower = (154, 0, 255)
colorUpper = (255, 255, 255)
width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
tailsize = 16
ballHistory = BallHistoryTest(tailsize)

table = True

while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    if not grabbed:
        break

    curr_frame = int(camera.get(cv2.CAP_PROP_POS_FRAMES))

    # first frame detect table
    if table:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        tableContours = table_detector(hsv)
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
    # TODO search by shape the ball
    if len(cnts) > 0:
        cmax = max(cnts, key=cv2.contourArea)
        M = cv2.moments(cmax)
        if M["m00"] > 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            ballHistory.add_ball(center, curr_frame)

# cleanup the camera and close any open windows
ballHistory.end_test()
camera.release()
cv2.destroyAllWindows()
