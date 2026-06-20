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

# Attrs to account for the restricted visible area imposed by 50mm cube
VISIBLE_WIDTH = 550 
VISIBLE_HEIGHT = 550
VISIBLE_OFFSET_X = (WIDTH - VISIBLE_WIDTH) // 2
VISIBLE_OFFSET_Y = (HEIGHT - VISIBLE_HEIGHT) // 2

def settings():
    py5.size(WIDTH,HEIGHT)

def setup():
    """Configures global styling and aquarium artifacts"""
    py5.color_mode(py5.HSB, 360, 100, 100) # Use HSB so we better control fish color & visibility
    set_mono_font()

    # create fish to swim throughout the tank
    _init_fish(5)
    
    # create seaweed to sway upon the floor
    _init_seaweed(10, 25)

def _init_fish(num_fish):
    """Initializes specified number of fish to render moving at random direction and speed"""
    for _ in range(num_fish):
        # My Fish
        fish_list.append(
            Fish(
                x=random.randint(MARGIN, VISIBLE_WIDTH - MARGIN),
                y=random.randint(MARGIN, VISIBLE_HEIGHT - MARGIN),
                speed=random.uniform(0.8, 1.2),
                angle=random.uniform(-math.pi, math.pi),
                margin=MARGIN,
                env_width=VISIBLE_WIDTH,
                env_height=VISIBLE_HEIGHT
            )
        )

def _init_seaweed(num_plants, min_spacing):
    """
    Initializes seaweed stalks, spaced properly with respect to provided inputs

    Args:
        num_plants: Number of separate stalks to render
        min_spacing: Number of pixels to enforce between rendered stalks
    """
    placed_x = []
    attempts = 0
    max_attempts = 1000 # prevents infinite loop

    while len(placed_x) < num_plants and attempts < max_attempts:
        attempts += 1
        candidate_x = random.randint(MARGIN, VISIBLE_WIDTH - MARGIN)

        # only init seaweed if position aligns to spacing constraints
        if all(abs(candidate_x - px) >= min_spacing for px in placed_x):
            placed_x.append(candidate_x)
            seaweed_list.append(
                Seaweed(
                    x=candidate_x,
                    height=random.randint(100,220),
                    env_height=VISIBLE_HEIGHT
                )
            )

def draw():
    """Renders background and manages sea critters"""
    py5.background(242,45,26) # deep blue

    # set translation layer for visible height/width
    py5.push_matrix()
    py5.translate(VISIBLE_OFFSET_X, VISIBLE_OFFSET_Y)

    # Draw seaweed first, behind fish
    for seaweed in seaweed_list:
        seaweed.display()
    
    # SWIM
    for fish in fish_list:
        fish.update()
        fish.display()
    
    py5.pop_matrix()

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
