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

tailsize = 10
pts = deque(maxlen=tailsize)
color = [(0, 0, 255),(0, 255, 255)]
colorIndx = 0

while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    if  not grabbed :
            camera.set(cv2.CAP_PROP_FRAME_COUNT, 0)
            camera.release()
            camera = cv2.VideoCapture(VIDEODEV)
            pts.clear()

            time.sleep(0.02)
            continue
     # show the frame to our screen
    #frame = resize(frame, width=600)
    #blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
     # show the frame to our screen
    frame = frame[130:385, 82:560]
    mask = cv2.inRange(frame, colorLower, colorUpper)
   # mask = cv2.erode(mask, None, iterations=2)
   # mask = cv2.dilate(mask, None, iterations=2)
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
        if center is not None :
             cv2.circle(center, (int(x), int(y)), 5,(0, 255, 0), -1)
        if M["m00"] > 0 :
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        #if radius > 0:
            # draw the minimum enclosing circle, yellow colour in BGR format(), thickness = 2
            cv2.circle(frame,center, 5,(0, 255, 0), -1)
            # draw the centroid,radius 5, red colour in BGR format(), thikness < 0 meaning that the circle is filled.

            #cv2.putText(frame, "Centroid  x: {}, y: {}".format(center[0], center[1]),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
             #           0.35, (0, 0, 255), 1)
            #cv2.putText(frame, "minEnclosing: x: {}, y: {}".format(int(x), int(y)),(10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX,
            #            0.35, (0, 0, 255), 1)
            ## IF Change of sense
            print center
            if (len(pts)> 1) and ((pts[0][0] - center[0])< 0) :
                pts.clear()
                colorIndx = (colorIndx+1) % 2
            pts.appendleft(center)


    # loop over the set of tracked points
    for i in xrange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
      #  cv2.circle(frame, pts[i], 5, (0, 0, 255), -1)
        thickness = 3
        cv2.line(frame,pts[i - 1], pts[i],color[colorIndx] , thickness)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF is ord('q'):
        break



# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
