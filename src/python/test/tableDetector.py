import cv2
import time
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="if present, path to the input video file")

args = vars(ap.parse_args())

if not args.get("video", False):
    VIDEODEV = 0
else:
    VIDEODEV = args["video"]

camera = cv2.VideoCapture(VIDEODEV);
assert camera.isOpened()

colorLower = (131, 0, 255)
colorUpper = (255, 255, 255)
while True:
    (grabbed, frame) = camera.read()
    frame[:25, :60] = 0
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=5)
    # mask = cv2.dilate(mask, None, iterations=5)
    # mask = cv2.erode(mask, None, iterations=5)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,  np.ones((8,8),np.uint8))


    cnts = cv2.findContours(mask.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
        sort = sorted(cnts, key=cv2.contourArea, reverse=True)
        cmax = sort[1]
        epsilon = 0.1 * cv2.arcLength(cmax, True)
        approx = cv2.approxPolyDP(cmax, epsilon, True)
        cv2.drawContours(frame, approx, -1, [0, 0, 0], 10)
        # cv2.polylines(frame,[approx],True,(0,0,0),10)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    if cv2.waitKey(1) & 0xFF is ord('q'):
        break

print(approx.__repr__())
np.save("table.npy", approx)
camera.release()
cv2.destroyAllWindows()
