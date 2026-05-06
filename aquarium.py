import platform
import random
import math
import py5

# local imports
from sea_creatures import Fish
from sea_plants import Seaweed

fish_list: list[Fish] = []
seaweed_list: list[Seaweed] = []

# Base canvas attrs. Aligns to Hyperpixel square display
WIDTH = 750
HEIGHT = 750
MARGIN = 25

def settings():
    py5.size(WIDTH,HEIGHT)

def setup():
    """
    Configures global styling and aquarium artifacts
    """
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
    
    # create seaweed to sway upon the floor
    for _ in range(18):
        seaweed_list.append(
            Seaweed(
                x = random.randint(MARGIN, WIDTH - MARGIN),
                height = random.randint(100,220)
            )
        )

def draw():
    """Renders background and manages sea critters"""
    py5.background(242,45,26) # deep blue

    # Draw seaweed first, behind fish
    for seaweed in seaweed_list:
        seaweed.display()
    
    # SWIM
    for fish in fish_list:
        fish.update()
        fish.display()

def set_mono_font():
    """Applies global mono font to rendered aquarium artifacts"""
    mono_font = py5.create_font(get_sys_mono_font(), 32)
    py5.text_font(mono_font)
    py5.text_align(py5.LEFT, py5.CENTER)

def get_sys_mono_font():
    """Determines mono font to apply to sketch depending on OS"""
    fonts = {
        "Linux": "Noto Sans Mono", # Linux font present on both Fedora and Bookworm
        "Darwin": "Menlo",         # MacOS sys default mono font
        "Windows": "Consolas"      # Obligatory Windows support
    }

    return fonts.get(platform.system(), "Courier New")

py5.run_sketch()
