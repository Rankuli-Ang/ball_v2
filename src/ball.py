"""The module contains Ball class."""


class Ball:
    """The target that the racket catches.
    Ball has center and borders coordinates,
    left and right border has only x axis coordinate,
    upper and down border has only y axis coordinate.
    Ball has vertical/horizontal acceleration and velocity.
    Ball has methods of changing its coordinates
    and velocity/acceleration reducing methods."""

    def __init__(self, start_x: int, start_y: int, radius: int):
        self.start_x: int = start_x
        self.start_y: int = start_y
        self.center_x: int = start_x
        self.center_y: int = start_y
        self.radius: int = radius

        self.left_border_x: int = 0
        self.right_border_x: int = 0
        self.upper_border_y: int = 0
        self.down_border_y: int = 0

        # a for acceleration, v for velocity
        self.horizontal_a: float = 0
        self.horizontal_v: float = 0

        self.vertical_a: float = 0
        self.vertical_v: float = 0

    def update_borders(self) -> None:
        """Updates the values of the border points of the ball."""
        self.left_border_x = self.center_x - self.radius
        self.right_border_x = self.center_x + self.radius
        self.upper_border_y = self.center_y - self.radius
        self.down_border_y = self.center_y + self.radius

    def horizontal_acceleration_decrease(self, hor_decrease) -> None:
        """Reduces horizontal acceleration of the ball."""
        self.horizontal_a -= hor_decrease

    def vertical_acceleration_decrease(self, vert_decrease) -> None:
        """Reduces vertical acceleration of the ball."""
        self.vertical_a -= vert_decrease

    def horizontal_shift(self, time: int) -> None:
        """Changes the position of the x-coordinate
        of the center of the ball in the process of movement."""
        self.center_x = round((self.horizontal_a * time) / 2 + self.horizontal_v * time + self.start_x)

    def vertical_shift(self, time: int) -> None:
        """Changes the position of the y-coordinate
         of the center of the ball in the process of movement."""
        self.center_y = round((self.vertical_a * time) / 2 + self.vertical_v * time + self.start_y)

    def primary_settings(self,
                         hor_v: int, hor_a: int,
                         vert_v: int, vert_a: int) -> None:
        """Sets primary speed characteristics
        and values of the ball borders."""
        self.update_borders()
        self.horizontal_v = hor_v
        self.horizontal_a = hor_a
        self.vertical_v = vert_v
        self.vertical_a = vert_a




