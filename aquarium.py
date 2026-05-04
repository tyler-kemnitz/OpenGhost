import random
import math
import py5
from sea_creatures import Fish

fish_list: list[Fish] = []
WIDTH = 750
HEIGHT = 750
MARGIN = 25

def settings():
    py5.size(WIDTH,HEIGHT)

def setup():
    py5.color_mode(py5.HSB, 360, 100, 100) # Use HSB so we better control fish color & visibility
    set_mono_font()

    # create new fish moving and random direction and speed
    for _ in range(5):
        # My Fish
        fish_list.append(
            Fish(
                x=random.randint(MARGIN, WIDTH - MARGIN),
                y=random.randint(MARGIN, HEIGHT - MARGIN),
                speed=random.uniform(0.8, 1.2),
                angle=random.uniform(-math.pi, math.pi),
                margin=MARGIN
            )
        )

def draw():
    """
    Sets background and renders each fish's updated velocity
    """
    py5.background(242,45,26)
    for fish in fish_list:
        fish.update()
        fish.display()

def set_mono_font():
    """
    Applies global mono font to rendered aquarium artifacts
    """
    noto_sans_mono = py5.create_font('Noto Sans Mono', 32)
    py5.text_font(noto_sans_mono)
    py5.text_align(py5.LEFT, py5.CENTER)

py5.run_sketch()
