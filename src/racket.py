class Racket:
    """Plane catching the ball."""

    def __init__(self, racket_plane: int, racket_center: int, racket_size: int):
        self.plane_x = racket_plane
        self.center_y = racket_center
        self.size = racket_size

    def aiming(self, world_height: int, aim_center: int):
        self.center_y = round(min(max(aim_center, 1), world_height))


