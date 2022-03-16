"""The module contains World class."""
import numpy as np
import cv2


class World:
    """World class visualizes the simulation.
    Visualization contains
    frames of the specified data collection field,
    ball and plane.
    """

    def __init__(self, height: int, width: int,
                 start_frame_y: int, end_frame_y: int, frame_color: tuple,
                 ball_color: tuple, ball_radius: int,
                 racket_color: tuple):

        self.height: int = height
        self.width: int = width

        self.start_frame_y: int = start_frame_y
        self.end_frame_y: int = end_frame_y
        self.frame_color: tuple = frame_color

        self.ball_color: tuple = ball_color
        self.ball_radius: int = ball_radius

        self.racket_color: tuple = racket_color

    def draw_frame(self, visualization) -> None:
        """Draws the edges of the specified data collection field."""

        for i in range(0, self.height):
            visualization[i][self.start_frame_y] = self.frame_color
            visualization[i][self.end_frame_y] = self.frame_color

    def draw_racket(self, visualization,
                    racket_plane: int, racket_center: int, racket_side: int) -> None:
        """Draws a racket."""

        for i in range(0, racket_side):
            visualization[min(self.height, racket_center + i)][racket_plane] = self.racket_color
            visualization[max(0, racket_center - i)][racket_plane] = self.racket_color

    def draw_ball(self, visualization, ball_x: int, ball_y: int) -> None:
        """Draws a ball."""
        cv2.circle(visualization, (ball_y, ball_x),
                   self.ball_radius, self.ball_color, thickness=-1)

    def visualize(self, ball_x: int, ball_y: int,
                  racket_plane: int, racket_center: int, racket_size: int) -> None:
        """Visualizes simulation
        and saves picture of the simulation to the "output" directory."""
        vis = np.zeros((self.height, self.width, 3), dtype='uint8')

        self.draw_frame(vis)
        self.draw_ball(vis, ball_x, ball_y)
        self.draw_racket(vis, racket_plane, racket_center, racket_size)

        cv2.imshow("vis", vis)
        cv2.imwrite("./output/vis.png", vis)
        cv2.waitKey(100)
