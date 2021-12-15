
class Ball:
    """An object that crosses the field,
    at the end of the field it is caught by the racket."""

    def __init__(self, start_x: int, start_y: int, radius: int):
        self.start_x = start_x
        self.start_y = start_y
        self.center_x = start_x
        self.center_y = start_y
        self.radius = radius

        self.left_border_x = self.center_x - self.radius
        self.right_border_x = self.center_x + self.radius
        self.upper_border_y = self.center_y - self.radius
        self.down_border_y = self.center_y + self.radius

        self.horizontal_a = 0
        self.horizontal_v = 0

        self.vertical_a = 0
        self.vertical_v = 0

    def update_borders(self):
        self.left_border_x = self.center_x - self.radius
        self.right_border_x = self.center_x + self.radius
        self.upper_border_y = self.center_y - self.radius
        self.down_border_y = self.center_y + self.radius

    def horizontal_acceleration_decrease(self, hor_decrease):
        self.horizontal_a -= hor_decrease

    def vertical_acceleration_decrease(self, vert_decrease):
        self.vertical_a -= vert_decrease

    def horizontal_shift(self, time: int):
        self.center_x = round((self.horizontal_a * time) / 2 + self.horizontal_v * time + self.start_x)

    def vertical_shift(self, time: int):
        self.center_y = round((self.vertical_a * time) / 2 + self.vertical_v * time + self.start_y)
