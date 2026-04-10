import random
import py5
from sea_creatures import Fish

fish_list: list[Fish] = []
WIDTH = 750
HEIGHT = 750
MARGIN = 25

def settings():
    py5.size(WIDTH,HEIGHT)

def setup():
    py5.background(0,0,0)
    set_mono_font()

    # create new fish moving and random direction and speed
    for _ in range(5):
        fish_list.append(
            Fish(random.randint(MARGIN, WIDTH),
                 random.randint(MARGIN, HEIGHT),
                 random.uniform(1.5, 2.5) * random.choice([-1, 1]),
                 random.uniform(-0.5, 0.5),
                 MARGIN)
        )

def draw():
    py5.background(0,0,0)
    for fish in fish_list:
        fish.update()
        fish.display()

def set_mono_font():
    noto_sans_mono = py5.create_font('Noto Sans Mono', 32)
    py5.text_font(noto_sans_mono)
    py5.text_align(py5.LEFT, py5.CENTER)

py5.run_sketch()
