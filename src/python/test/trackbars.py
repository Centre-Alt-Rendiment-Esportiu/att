import numpy as np
import cv2
import time
import argparse

def setup_trackbars(range_filter):
    cv2.namedWindow("Trackbars", 0)
    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = 0 if i == "MIN" else 255
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, lambda x : None)



def get_trackbar_values(range_filter):
    values = {}

    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values["%s_%s" % (j, i)] = v
    return values




ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="if present, path to the input video file")

args = vars(ap.parse_args())

if not args.get("video", False):
    VIDEODEV = 0
else:
    VIDEODEV = args["video"]


camera = cv2.VideoCapture(VIDEODEV); assert camera.isOpened()
setup_trackbars('HSV')
while True:
        (grabbed, frame) = camera.read()
        if  not grabbed :
            camera.set(cv2.CAP_PROP_FRAME_COUNT, 0)
            time.sleep(0.2)
            continue
        frame_to_thresh = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        v = get_trackbar_values('HSV')
        thresh = cv2.inRange(frame_to_thresh, (v['H_MIN'], v['S_MIN'], v['V_MIN']), (v['H_MAX'], v['S_MAX'], v['V_MAX']))
        cv2.imshow("Original", frame)
        cv2.imshow("Thresh", thresh)
        if cv2.waitKey(1) & 0xFF is ord('q'):
            break

print("Lower = (%d,%d,%d)" % (v['H_MIN'], v['S_MIN'], v['V_MIN']))
print("Upper = (%d,%d,%d)" % (v['H_MAX'], v['S_MAX'], v['V_MAX']))
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()