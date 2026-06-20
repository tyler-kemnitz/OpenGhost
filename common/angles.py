import math

def normalize_angle(angle: float) -> float:
    """Wrap an angle into the range (-pi, pi]."""
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle <= -math.pi:
        angle += 2 * math.pi
    return angle

def angle_delta(current: float, target: float) -> float:
    """Return the shortest signed angular distance from current to target."""
    return normalize_angle(target - current)
