"""The module contains class Racket."""


class Racket:
    """Racket is a plane that catches the ball.
    Racket has coordinates of the center plane
    and side - is a distance from center of the plane to the edge.
    Aiming method - racket gets target coordinate in y axis
    and changes racket center coordinates to the target."""

    def __init__(self, racket_plane: int, racket_center: int, racket_side: int):
        self.plane_x: int = racket_plane
        self.center_y: int = racket_center
        self.side: int = racket_side

    def aiming(self, world_height: int, aim_center_y: int) -> None:
        """Moves racket to the received 'y' coordinate."""
        self.center_y = round(min(max(aim_center_y, 1), world_height))

    def get_racket_upper_edge_y(self) -> int:
        """Returns the coordinate of the upper edge of the racket."""
        upper_edge = self.center_y - self.side
        return upper_edge

    def get_racket_down_edge_y(self) -> int:
        """Returns the coordinate of the down edge of the racket."""
        down_edge = self.center_y + self.side
        return down_edge
