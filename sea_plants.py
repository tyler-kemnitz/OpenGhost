import py5
import math
import random

class Seaweed:
    """Class representing seaweed rendered using Bezier segments"""
    # Number of Bezier segments composing the stalk
    SEGMENTS = 4

    # In pixels, maximum horizontal displacement of stalk tip at peak sway
    SWAY_AMPLITUDE = 12

    # Oscillation speed, in radius per frame
    # Lower = slower sway, Higher = rapid sway
    SWAY_SPEED = 0.025

    # per-segment lateral bulge of control points, in pixels
    # this creates visible curvature within each segment
    SEGMENT_CURVE = 10

    # HSB color values (green seaweed)
    HUE = 120
    SATURATION = 70
    BRIGHTNESS = 55

    def __init__(self, x, height):
        """
        Args:
            x: Horizontal anchor position of the base
            height: Length of stalk, in pixels
        """
        self.x = x
        self.height = height

        # random phase so multiple stalks don't sway together
        self._phase = random.uniform(0, 2 * math.pi)
    
    ##
    # Public Interface
    ##

    def display(self):
        """Draw seaweed stalk at current sway position"""
        py5.push_style() # Apply scoped styling for seaweed
       
        py5.no_fill()
        py5.stroke(self.HUE, self.SATURATION, self.BRIGHTNESS)
        py5.stroke_weight(3)

        # Set up attrs to start drawing segments
        base_y = py5.height

        # TODO::Explain usage of sin() here
        sway = self.SWAY_AMPLITUDE * math.sin(
            py5.frame_count * self.SWAY_SPEED + self._phase
        )

        segment_height = self.height / self.SEGMENTS

        py5.begin_shape()
        py5.vertex(self.x, base_y)

        for i in range(self.SEGMENTS):
            # compute y-positions for segment's two control points and its end anchor
            cp1_y = base_y - (i * segment_height + (segment_height / 3))
            cp2_y = base_y - (i * segment_height + 2 * (segment_height / 3))
            end_y = base_y - (i + 1) * segment_height

            # normalized height: 0.0 at base, 1.0 at tip
            # Scaling the x offset by this value ensures the base stays fixed
            # while the tip sways the full SWAY_AMPLITUDE distance
            cp1_t = (base_y - cp1_y) / self.height
            cp2_t = (base_y - cp2_y) / self.height
            end_t = (base_y - end_y) / self.height

            # Alternate bulge direction to produce an S-curve
            curve_sign = 1 if i % 2 == 0 else -1
            lateral = self.SEGMENT_CURVE * curve_sign

            py5.bezier_vertex(
                self.x + sway * cp1_t + lateral, cp1_y,
                self.x + sway * cp2_t + lateral, cp2_y,
                self.x + sway * end_t, end_y
            )
        
        py5.end_shape()
        py5.pop_style()
