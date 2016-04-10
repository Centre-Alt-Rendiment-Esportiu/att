# import the necessary packages

from collections import deque
import numpy as np
import cv2
import time


#Convenience resize function
def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized

#VIDEODEV = 0
VIDEODEV = "./partida.avi"


camera = cv2.VideoCapture(VIDEODEV); assert camera.isOpened()

colorLower = (251,251,251)
colorUpper = (255,255,255)

tailsize = 16
pts = deque(maxlen=tailsize)
color = [(0, 0, 255),(0, 255, 255)]
colorIndx = 0

while True:
    # grab the current frame
    (grabbed, frameWhole) = camera.read()

    if  not grabbed :
            camera.set(cv2.CAP_PROP_FRAME_COUNT, 0)
            camera.release()
            camera = cv2.VideoCapture(VIDEODEV)
            pts.clear()

            time.sleep(0.02)
            continue
     # show the frame to our screen
    frame = frameWhole[133:380, 85:555]
    mask = cv2.inRange(frame, colorLower, colorUpper)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    # only proceed if at least one contour was found
    reset  = True
    if len(cnts) > 0:
        cmax = max(cnts, key=cv2.contourArea)
        M = cv2.moments(cmax)
        if M["m00"] > 0 :
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.circle(frame,center, 5,(0, 255, 0), -1)
            # calculate direction of ball, paint it ,if change clear
            if (len(pts)> 0) and ((pts[0][0] - center[0])< 0) :
                if colorIndx != 0 :
                    colorIndx = 0
                    pts.clear()
            elif (len(pts)> 0) and ((pts[0][0] - center[0]) > 0) :
                 if colorIndx != 1 :
                    colorIndx = 1
                    pts.clear()
            pts.appendleft(center)

    # loop over the set of tracked points
    for i in xrange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue
        thickness = 3
        cv2.line(frame,pts[i - 1], pts[i],color[colorIndx] , thickness)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("AllFrame", frameWhole)
    time.sleep(0.5)
    if cv2.waitKey(1) & 0xFF is ord('q'):
        break



# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
