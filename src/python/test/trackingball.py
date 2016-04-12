# import the necessary packages

from collections import deque
import numpy as np
import cv2
import time
import argparse



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



def tableDetector(frame):

    mask = cv2.inRange(frame, (131,0,255), (255,255,255))
    mask = cv2.dilate(mask, None, iterations=5)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
            sort = sorted(cnts, key=cv2.contourArea,reverse=True)
            cmax = sort[1]
            epsilon = 0.1*cv2.arcLength(cmax,True)
            approx = cv2.approxPolyDP(cmax,epsilon,True)
    return approx

ap = argparse.ArgumentParser()

ap.add_argument("-v", "--video",
	help="if present, path to the input video file")

ap.add_argument("-o", "--output",
	help="if present, path to the output video file")

ap.add_argument("-t", "--table",
	help="if present, table points")

ap.add_argument('-l','--loop', dest='LOOP', action='store_true')
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

camera = cv2.VideoCapture(VIDEODEV); assert camera.isOpened()

colorLower = (154,0,255)
colorUpper = (255,255,255)
width = camera.get(3)
height = camera.get(4)
tailsize = 16
pts = deque(maxlen=tailsize)
color = [(0, 0, 255),(0, 255, 255)]
colorIndx = 0



if not args["table"]:
    table = True
else:
    table = False
    tableContours = np.load(args["table"])
    maskTable = np.zeros((height,width),np.uint8)
        # 0 is table, 1 is background
    cv2.fillConvexPoly(maskTable, tableContours, 1)
    maskTable = np.dstack(3*(maskTable,))

if OUTPUT:
        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        writer = cv2.VideoWriter(OUTPUT, fourcc, 20, (int(width),int(height)),True)

while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    if not grabbed :
        if LOOP:
            camera.set(cv2.CAP_PROP_FRAME_COUNT, 0)
            camera.release()
            camera = cv2.VideoCapture(VIDEODEV)
            pts.clear()
            time.sleep(0.02)
            continue
        else :
            break

    #first frame detect table

    if table:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        tableContours = tableDetector(hsv)
        maskTable = np.zeros((height,width),np.uint8)
        # 0 is table, 1 is background
        cv2.fillConvexPoly(maskTable, tableContours, 1)
        maskTable = np.dstack(3*(maskTable,))
        table = False

    #add maskTable to frame
    frameTable = frame*maskTable
    hsv = cv2.cvtColor(frameTable, cv2.COLOR_BGR2HSV)

    #find white color mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)

    mask= cv2.dilate(mask, None, iterations=2)
    #mask= cv2.erode(mask, None, iterations=1)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    # only proceed if at least one contour was found
    reset  = True
    if len(cnts) > 0:
        cmax = max(cnts, key=cv2.contourArea)
        #if cv2.contourArea(cmax)>20 :
        #print cv2.contourArea(cmax)
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
    if len(pts)> 0:
        cv2.circle(frame,pts[0], 5,(0, 255, 0), -1)
        for i in xrange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
            if pts[i - 1] is None or pts[i] is None:
                continue
            thickness = 3
            cv2.line(frame,pts[i - 1], pts[i],color[colorIndx] , thickness)
            cv2.circle(frame,pts[i], 5,(0, 255, 0), -1)

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
