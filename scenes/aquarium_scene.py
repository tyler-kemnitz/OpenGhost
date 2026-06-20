import math
import random
import py5

from entities.sea_creatures import Fish
from entities.sea_plants import Seaweed
from common.fonts import set_mono_font
from scenes.scene import Scene

class AquariumScene(Scene):
    """Owns and updates every drawable entity in the aquarium"""

    BACKGROUND_COLOR = (242, 45, 26) # In HSB

    def __init__(self, width: int, height: int, margin: int=25)
        self.width = width
        self.height = height
        self.margin = margin

        self.fish_list = list[Fish] = []
        self.seaweed_list = list[Seaweed] = []

    ##
    # Public Interface
    ##
    def setup(self, num_fish: int, num_seaweed: int, seaweed_spacing: int):
        """Configure base attributes and initialize sea entities"""
        py5.color_mode(py5.HSB, 360, 100, 100)
        set_mono_font()

        self._init_fish(num_fish)
        self._init_seaweed(num_seaweed, seaweed_spacing)

    def update(self):
        """Advance every entity by one frame"""
        for fish in self.fish_list:
            fish.update()

    def display(self):
        """Render scene for all sea entities"""
        py5.background(*self.BACKGROUND_COLOR)

        # Render seaweed first so it's behind the fish
        for seaweed in self.seaweed_list:
            seaweed.display()
        
        for fish in self.fish_list:
            fish.display()
    
    def _init_fish(self, num_fish):
        """
        Initializes specified number of fish to render moving at random direction and speed
        
        Args:
            num_fish: Number of fish to render
        """
        for _ in range(num_fish):
            # My Fish
            self.fish_list.append(
                Fish(
                    x=random.randint(self.margin, self.width - self.margin),
                    y=random.randint(self.margin, self.height - self.margin),
                    speed=random.uniform(0.8, 1.2),
                    angle=random.uniform(-math.pi, math.pi),
                    margin=self.margin,
                    env_width=self.width,
                    env_height=self.height
                )
            )
    
    def _init_seaweed(self, num_plants, min_spacing):
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
            candidate_x = random.randint(self.margin, self.width - self.margin)

            # only init seaweed if position aligns to spacing constraints
            if all(abs(candidate_x - px) >= min_spacing for px in placed_x):
                placed_x.append(candidate_x)
                self.seaweed_list.append(
                    Seaweed(
                        x=candidate_x,
                        height=random.randint(100,220),
                        env_height=self.height
                    )
                )
