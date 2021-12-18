class Racket:
    """Plane catching the ball."""

    def __init__(self, racket_plane: int, racket_center: int, racket_size: int):
        self.plane_x = racket_plane
        self.center_y = racket_center
        self.size = racket_size

    def aiming(self, world_height: int, aim_center_y: int) -> None:
        """Moves racket to the received 'y' coordinate."""
        self.center_y = round(min(max(aim_center_y, 1), world_height))

    def get_racket_upper_edge_y(self) -> int:
        upper_edge = self.center_y - self.size
        return upper_edge

    def get_racket_down_edge_y(self) -> int:
        down_edge = self.center_y + self.size
        return down_edge
