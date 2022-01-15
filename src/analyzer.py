import numpy as np
import cv2


class Analyzer:
    """A class that analyzes the movement of the ball
     and transfers the coordinates to the racket."""

    def __init__(self, start_frame: int, end_frame: int):
        self.start_frame = start_frame
        self.end_frame = end_frame

    def analyze(self) -> tuple:
        """Detected ball in the picture of the simulation
        and returns ball coordinates."""
        raw_img = cv2.imread("./output/vis.png", cv2.IMREAD_GRAYSCALE)
        gray = raw_img[:, self.start_frame:self.end_frame]

        gray = cv2.medianBlur(gray, 5)

        rows = gray.shape[0]
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, minDist=rows/8,
                                   param1=100, param2=1,
                                   minRadius=1, maxRadius=30)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                cv2.circle(gray, center, 1, (0, 100, 100), 3)
                radius = i[2]
                cv2.circle(gray, center, radius, (255, 0, 255), 3)
                cv2.imshow("detected_circle", gray)
                cv2.waitKey(100)
                print('ball coordinates', center)
                return center
