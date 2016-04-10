import cv2
import time

VIDEODEV = "./partida.avi"
#VIDEODEV = 0


camera = cv2.VideoCapture(VIDEODEV); assert camera.isOpened()

colorLower = (230,230,230)
colorUpper = (255,255,255)
while True:
        (grabbed, frame) = camera.read()
        if not grabbed :
            camera.set(cv2.CAP_PROP_FRAME_COUNT, 0)
            camera.release()
            camera = cv2.VideoCapture(VIDEODEV)
            time.sleep(0.02)
            continue

        mask = cv2.inRange(frame, colorLower, colorUpper)
        mask = cv2.dilate(mask, None, iterations=4)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:

            sort = sorted(cnts, key=cv2.contourArea,reverse=True)
            cmax = sort[1]
            epsilon = 0.1*cv2.arcLength(cmax,True)
            approx = cv2.approxPolyDP(cmax,epsilon,True)
            cv2.drawContours(frame,approx,-1,[0,0,0],10)
            #cv2.polylines(frame,[approx],True,(0,0,0),10)
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)
        time.sleep(0.5)
        if cv2.waitKey(1) & 0xFF is ord('q'):
            break

print approx.__repr__()
camera.release()
cv2.destroyAllWindows()

