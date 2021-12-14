import numpy as np
import cv2


class World:
    """A class that visualizes the movement of simulation objects."""

    def __init__(self, height: int, width: int,
                 start_frame_y: int, end_frame_y: int, frame_color: tuple,
                 ball_color: tuple, ball_radius: int,
                 racket_color: tuple):

        self.height: int = height
        self.width: int = width

        self.start_frame_y = start_frame_y
        self.end_frame_y = end_frame_y
        self.frame_color = frame_color

        self.ball_color = ball_color
        self.ball_radius = ball_radius

        self.racket_color = racket_color

    def draw_frame(self, visualization):
        start_frame_counter = 0
        end_frame_counter = 0

        while start_frame_counter < self.height:
            visualization[start_frame_counter][self.start_frame_y] = self.frame_color
            start_frame_counter += 1

        while end_frame_counter < self.height:
            visualization[end_frame_counter][self.end_frame_y] = self.frame_color
            end_frame_counter += 1

    def draw_racket(self, visualization,
                    racket_plane: int, racket_center: int, racket_size: int):
        counter = 0
        while counter <= racket_size:
            if racket_center + counter < self.height:
                visualization[racket_center + counter][racket_plane] = self.racket_color
                if racket_center - counter > 0:
                    visualization[racket_center - counter][racket_plane] = self.racket_color
            counter += 1

    def draw_ball(self, visualization, ball_x: int, ball_y: int):
        cv2.circle(visualization, (ball_y, ball_x), self.ball_radius, self.ball_color, thickness=-1)

    def visualize(self, ball_x: int, ball_y: int,
                  racket_plane: int, racket_center: int, racket_size: int):
        vis = np.zeros((self.height, self.width, 3), dtype='uint8')

        self.draw_frame(vis)
        self.draw_ball(vis, ball_x, ball_y)
        self.draw_racket(vis, racket_plane, racket_center, racket_size)

        cv2.imshow("vis", vis)
        cv2.imwrite("./output/vis.png", vis)
        cv2.waitKey(100)
