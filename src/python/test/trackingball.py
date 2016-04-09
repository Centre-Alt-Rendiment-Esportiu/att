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

VIDEODEV = 0


camera = cv2.VideoCapture(VIDEODEV); assert camera.isOpened()


colorLower = (166,15,81)
colorUpper =  (189,219,119)
tailsize = 64
pts = deque(maxlen=tailsize)


while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
     # show the frame to our screen
    #frame = resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
     # show the frame to our screen
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        cmax = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(cmax)
        M = cv2.moments(cmax)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the minimum enclosing circle, yellow colour in BGR format(), thickness = 2
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            # draw the centroid,radius 5, red colour in BGR format(), thikness < 0 meaning that the circle is filled.
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            cv2.putText(frame, "Centroid  x: {}, y: {}".format(center[0], center[1]),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.35, (0, 0, 255), 1)
            cv2.putText(frame, "minEnclosing: x: {}, y: {}".format(int(x), int(y)),(10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.35, (0, 0, 255), 1)


    pts.appendleft(center)

    # loop over the set of tracked points
    for i in xrange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(tailsize / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF is ord('q'):
        break



# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
