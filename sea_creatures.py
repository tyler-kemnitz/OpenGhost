import py5
import math
import random

class Fish:
    # How quickly the fish turns toward its target angle (radians per frame).
    # Lower = lazier, wider arcs. Higher = snappier turns.
    TURN_RATE = 0.02

    # When a fish enters the wall-avoidance zone (margin + WALL_SENSE_DISTANCE),
    # it starts steering away before actually hitting the boundary.
    WALL_SENSE_DISTANCE = 80

    # Maximum random nudge (radians) applied to the target angle each wander event.
    WANDER_NUDGE = math.pi / 6  # 30 degrees

    def __init__(self, x, y, speed, angle, margin):
        """
        Args:
            x, y: Initial position
            speed: Scalar speed in pixels per frame (always positive)
            angle: Initial heading in radians, 0 = right, pi = left
            margin: Hard boundary the fish must stay inside
        """
        self.speed = speed
        self.angle= angle
        self.target_angle = angle # heading fish is steering toward
        self.margin = margin

        # ensure sprite is not spawned outside x/y constraints
        self.sprite_width = py5.text_width(self._sprite())
        self.sprite_height = py5.text_ascent() + py5.text_descent()

        self.x = py5.constrain(x, self.margin, py5.width - self.margin - self.sprite_width)
        self.y = py5.constrain(y, self.margin, py5.height - self.margin - self.sprite_height)

        self._wander_cooldown = 0 # Prevents fish from changing direction every frame

    ##
    # Public Interface
    ##
    def update(self):
        """Advance fish by one frame, steer, move, then wander"""
        self._steer()
        self._move()
        self._wander()

    def display(self):
        py5.fill(255,255,255) # Set fish color
        py5.text(self._sprite(), self.x, self.y)

    ###
    # Private Helpers
    ###
    def _steer(self):
        """
        Nudge current angle toward target_angle by at most TURN_RATE radians,
        then check whether wall proximity demands override
        """
        # Get shortest angular path to current target
        delta = _angle_delta(self.angle, self.target_angle)
        self.angle += py5.constrain(delta, -self.TURN_RATE, self.TURN_RATE)
        self.angle = _normalize_angle(self.angle)

        ## Wall Avoidance
        # If fish is within turn margin for any wall, apply a new target angle so the fish curves away naturally
        wall_target = self._get_wall_avoidance_angle()
        if wall_target is not None:
            wall_delta = _angle_delta(self.angle, wall_target)
            # apply wall steering at twice normal turn rate so fish reacts quickly enough to not clip boundary
            self.angle += py5.constrain(wall_delta, -self.TURN_RATE * 1.2, self.TURN_RATE * 1.2)

            # update target angle so fish does not fight wall correction on next frame
            self.target_angle = self.angle

    def _move(self):
        """
        Translate position along current heading, then clamp to environment boundaries
        """
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        right_bound = py5.width - self.margin - self.sprite_width
        bottom_bound = py5.height - self.margin - self.sprite_height

        self.x = py5.constrain(self.x, self.margin, right_bound)
        self.y = py5.constrain(self.y, self.margin, bottom_bound)

    def _wander(self):
        if self._wander_cooldown > 0:
            self._wander_cooldown -= 1
            return

        if random.random() < 0.008:
            # How vertical is the current heading? sin(angle) is 1.0 when pointing
            # straight up/down, 0.0 when pointing horizontally.
            vertical_amount = abs(math.sin(self.angle))

            # Bias the nudge toward horizontal proportionally. When nearly vertical,
            # this is a strong push; when already horizontal, it's almost neutral.
            horizontal_bias = vertical_amount * self.WANDER_NUDGE

            # The sign of the bias points away from vertical (toward 0 or ±π).
            # math.copysign gives us the correct direction without branching.
            bias_sign = -math.copysign(1.0, math.sin(self.angle))
            biased_nudge = random.uniform(-self.WANDER_NUDGE, self.WANDER_NUDGE) + (bias_sign * horizontal_bias)

            self.target_angle = _normalize_angle(self.angle + biased_nudge)
            self._wander_cooldown = random.randint(120, 300)

    def _get_wall_avoidance_angle(self):
        """
        Return a suggested heading angle used to steer away from nearby walls,
        or None if fish is not close to any wall.
        """
        turn_sense = self.margin + self.WALL_SENSE_DISTANCE
        right_bound = py5.width - self.margin - self.sprite_width - self.WALL_SENSE_DISTANCE
        bottom_bound = py5.height - self.margin - self.sprite_height - self.WALL_SENSE_DISTANCE

        near_left = self.x < turn_sense
        near_right = self.x > right_bound
        near_top= self.y < turn_sense
        near_bottom = self.y > bottom_bound

        if not any([near_left, near_right, near_top, near_bottom]):
            return None

        # aim toward center of environment with vertical bias so fish arcs instead of turning sharply
        cx = py5.width / 2
        cy = py5.height / 2

        return math.atan2(cy - self.y, cx - self.x)

    def _sprite(self):
        """Return ASCII sprite matching the fish's current heading"""
        # cos(angle) > 0 means fish is moving to the right
        return '>\')))>' if math.cos(self.angle) >= 0 else '<\'(((<'

###
# Module-level angle utilities
###
def _normalize_angle(angle):
    """Wrap an angle into (-pi, pi]"""
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle <= -math.pi:
        angle += 2 * math.pi
    return angle

def _angle_delta(current: float, target: float) -> float:
    """Return shortest signed angular distance from current to target"""
    return _normalize_angle(target - current)
