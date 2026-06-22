import py5
import math
import random

class Bubble:
    """
    A single rising bubble with a three-phase lifecycle:
    growth, rising, and fade-out
    """

    # net upward acceleratoin in pixels per frame sq, applied every rising frame
    BUOYANCY_ACCEL: float = 0.08

    # linear drag coefficient. per frame drag is applied as vy = vy * (1 - DRAG_COEFFICIENT) - BUOYANCY_ACCEL
    # specific to aquarium.py
    DRAG_COEFFICIENT: float = 0.04

    # pixels added to radius each frame during growth phase
    GROWTH_RATE: float = 0.4

    # Peak horizontal displacement of the sinusoidal wobble, in pixels
    DRIFT_AMPLITUDE: float = 2.5

    # angular frequency of the wobble, radians/frame
    DRIFT_FREQUENCY: float = 0.10
    
    # pixels below the top margin at which fade-out starts
    FADE_ZONE: int = 80

    def __init__(self, x: float, y: float, radius: float, margin: int):
        """
        Args:
            x:       Horizontal spawn position in pixels
            y:       Vertical spawn position
            radius:  The bubble's full radius once the growth phase ends.
            margin:  Top boundary y-value; bubble is marked dead when it crosses this.
        """

        self.origin_x = x  # fixed horizontal anchor for drift calc
        self.x = x
        self.y = y
        self.target_radius = radius
        self.radius = 0.0 # start at zero, expand during growth phase
        self.margin = margin

        self._vy = 0.0 # vertical velocity in pixels/frame

        # per-bubble phase offset so a stream doesn't have sync'd wobbling
        self._phase = random.uniform(0.0, 2.0 * math.pi)

        self._frame_born = py5.frame_count # age is relative to birth frame, not global clock
        self._growing = True
        self._alive = True
    
    ##
    # Public Interface
    ##

    @property
    def is_alive(self) -> bool:
        return self._alive

    def update(self) -> None:
        """Advance bubble by one frame"""
        if self._growing:
            self._grow()
        else:
            self._apply_physics()
            self._apply_drift()
            self._check_bounds()
    
    def display(self) -> None:
        """Render the bubble: outline, fill, highlight"""
        alpha = self._compute_alpha()

        # scope bubble styling to 
        py5.push_style()
        
        py5.stroke_weight(1.5)
        py5.stroke(210, 20, 92, alpha) # pale blue-white

        # faint fill to help add spherical appearance
        py5.fill(210, 8, 98, int(alpha * 0.12))
        py5.circle(self.x, self.y, self.radius * 2)

        # add specular highlight
        if self.radius >= (self.target_radius / 3):
            py5.no_stroke()
            py5.fill(210, 5, 100, int(alpha) * 0.70)
            highlight_d = self.radius * 0.55
            offset = self.radius * 0.30
            py5.circle(self.x - offset, self.y - offset, highlight_d)

        py5.pop_style()
    
    ##
    # Private Helpers
    ##

    def _grow(self) -> None:
        """Expand radius toward target. Transition to rising phase when complete"""
        self.radius = min(self.radius + self.GROWTH_RATE, self.target_radius)
        if self.radius >= self.target_radius:
            self._growing = False

    def _apply_physics(self) -> None:
        """
        Euler integration of buoyancy and linear drag
        """
        self._vy = self._vy * (1.0 - self.DRAG_COEFFICIENT) - self.BUOYANCY_ACCEL
        self.y += self._vy
    
    def _apply_drift(self) -> None:
        """
        Sinusoidal horizontal wobble to mimic sideways reaction forces acting on bubble
        """
        age = py5.frame_count - self._frame_born
        self.x = self.origin_x + self.DRIFT_AMPLITUDE + math.sin(
            age * self.DRIFT_FREQUENCY + self._phase
        )
    
    def _check_bounds(self) -> None:
        """Mark bubble as dead once its top edge clears top margin"""
        if self.y - self.radius < self.margin:
            self._alive = False
    
    def _compute_alpha(self) -> int:
        """
        Return an alpha value in 0-255.
 
        Growing:   fades in proportionally to growth progress.
        Rising:    full opacity until the bubble enters FADE_ZONE.
        Fade-out:  linear drop to 0 as the bubble reaches the top margin.
        """
        if self._growing:
            return int(255.0 * (self.radius / max(self.target_radius, 1.0)))
 
        dist_from_top = self.y - self.margin
        if dist_from_top < self.FADE_ZONE:
            return int(255.0 * max(dist_from_top / self.FADE_ZONE, 0.0))
 
        return 255

class BubbleStream:
    """Manages a vertical column of rising bubbles from a fixed anchor"""

    def __init__(
            self,
            x: int,
            spawn_y: int,
            margin: int,
            spawn_delay: int = 90,
            max_bubbles: int = 12,
            min_radius: float = 4.0,
            max_radius: float = 9.0,
    ) -> None:
        """
        Args:
            x:            Horizontal center of the stream (pixels).
            spawn_y:      Y-coordinate where new bubbles are created.
                          Pass HEIGHT - MARGIN to anchor at the tank floor.
            margin:       Top boundary of the tank passed to each Bubble.
            spawn_delay:  Frames between successive spawns.  To convert from
                          seconds multiply by the sketch frame rate (default 60 fps):
                            30  frames → ~0.5 s  (dense stream)
                            90  frames → ~1.5 s  (moderate trickle, default)
                            180 frames → ~3.0 s  (sparse, occasional bubbles)
            max_bubbles:  Hard cap on simultaneous live bubbles.  With defaults
                          (spawn_delay=90, terminal velocity=1.5 px/frame, tank
                          height 700 px) a bubble takes ~467 frames to rise, so
                          at most ~5 are alive at once — well under the cap.
            min_radius:   Lower bound of the random bubble radius range (pixels).
            max_radius:   Upper bound of the random bubble radius range (pixels).
        """
        self.x = x
        self.spawn_y = spawn_y
        self.margin = margin
        self.spawn_delay = spawn_delay
        self.max_bubbles = max_bubbles
        self.min_radius = min_radius
        self.max_radius = max_radius
 
        self._bubbles = []
        self._spawn_countdown = 0  # Frames remaining until the next spawn

    ## 
    # Public interface
    ##
 
    def update(self) -> None:
        """Remove dead bubbles, tick survivors, then spawn on schedule."""
        # List comprehension cull — cheaper than repeated list.remove() calls
        self._bubbles = [b for b in self._bubbles if b.is_alive]
 
        for bubble in self._bubbles:
            bubble.update()
 
        if self._spawn_countdown <= 0:
            if len(self._bubbles) < self.max_bubbles:
                self._spawn()
            # Always reset the countdown — even if the stream is at capacity —
            # so it doesn't attempt to catch up with a burst of spawns.
            self._spawn_countdown = self.spawn_delay
        else:
            self._spawn_countdown -= 1
 
    def display(self) -> None:
        """Draw all live bubbles."""
        for bubble in self._bubbles:
            bubble.display()
 
    ##
    # Private helpers
    ##
 
    def _spawn(self) -> None:
        """Create a new bubble with randomised size and a small horizontal jitter."""
        radius = random.uniform(self.min_radius, self.max_radius)
        # Small x jitter so bubbles don't rise in a perfectly straight column.
        jitter_x = random.uniform(-5.0, 5.0)
        self._bubbles.append(
            Bubble(
                x=self.x + jitter_x,
                y=float(self.spawn_y),
                radius=radius,
                margin=self.margin,
            )
        )
