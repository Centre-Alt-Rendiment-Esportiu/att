import numpy as np
import cv2
import glob


class CameraCalibrate:
    def __init__(self):
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        row, col = 7, 7
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((row * col, 3), np.float32)
        objp[:, :2] = np.mgrid[0:row, 0:col].T.reshape(-1, 2)
        # Arrays to store object points and image points from all the images.
        objpoints = []  # 3d point in real world space
        imgpoints = []  # 2d points in image plane.

        images = glob.glob('*.png')  # TODO hardcode images
        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (row, col), None)
            # If found, add object points, image points (after refining them)
            if ret:
                objpoints.append(objp)
                cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners)
                # Draw and display the corners
                cv2.drawChessboardCorners(img, (row, col), corners, ret)
                cv2.imshow('img', img)
                cv2.waitKey(1)

        ret, self.mtx, self.dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    def undistort(self, frame):
        img = frame
        h, w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w, h), 1, (w, h))
        # undistort
        dst = cv2.undistort(img, self.mtx, self.dist, None, newcameramtx)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
        return dst
