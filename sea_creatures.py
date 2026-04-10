import py5
import random

class Fish:
    def __init__(self, x, y, dx, dy, margin):
        # Set direction and attrs dependent on dx
        self.dx = dx
        self.dy = dy
        self.sprite_width = py5.text_width(self.get_sprite())
        self.sprite_height = py5.text_ascent() + py5.text_ascent()

        self.margin = margin # turn margin

        # ensure sprite is not spawned outside x/y constraints
        self.x = py5.constrain(x, self.margin, py5.width - (self.margin + self.sprite_width))
        self.y = py5.constrain(y, self.margin, py5.height - (self.margin + self.sprite_height))

        # Timer for random direction changes
        self.turn_cooldown = 0

    def update(self):
        # Update position determine direction change
        self.x += self.dx
        self.y += self.dy
        self.change_direction()

    def display(self):
        py5.fill(255,255,255) # Set fish color
        py5.text(self.get_sprite(), self.x, self.y)

    def change_direction(self):
        lower_bound = self.margin
        upper_bound_x = py5.width - self.sprite_width
        upper_bound_y = py5.height - self.sprite_height

        # Keep within aquarium walls
        force_change = False
        if self.x <= lower_bound or self.x > (upper_bound_x - self.margin):
            self.dx *= -1
            force_change = True
        if self.y <= lower_bound or self.y >= (upper_bound_y - self.margin):
            self.dy *= -1
            force_change = True

        # Change x direction based on cooldown + 0.1% chance per frame
        if self.turn_cooldown > 0:
            self.turn_cooldown -= 1
        if not force_change:
            if self.turn_cooldown <= 0 and random.random() < 0.001:
                self.dx *= -1
                self.turn_cooldown = random.randint(180, 360) # every 180-360 frames

    def get_sprite(self):
        if self.dx is None:
            return None
        if self.dx > 0:
            return '>\')))>'
        return '<\'(((<'
