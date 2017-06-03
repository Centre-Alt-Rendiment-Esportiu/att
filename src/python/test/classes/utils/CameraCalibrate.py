import numpy as np
import cv2


class CameraCalibrate:
    def __init__(self):
        f_x, f_y = 1.0424e+03, 813.7234
        c_x, c_y = 485.1304, -89.7278
        self.cam_matrix = np.matrix([[f_x, 0, c_x], [0, f_y, c_y], [0, 0, 1]])

        k1, k2, k3 = -0.3692, -0.0680, 0.1172
        p1, p2 = 0.1360, -0.0018
        self.coeffs = np.asarray([k1, k2, p1, p2, k3])

    def undistort(self, frame):
        img = frame
        h, w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.cam_matrix, self.coeffs, (w, h), 1, (w, h))
        # undistort
        dst = cv2.undistort(img, self.cam_matrix, self.coeffs, None, newcameramtx)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
        return dst
