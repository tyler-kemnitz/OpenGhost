import py5

from scenes.aquarium_scene import AquariumScene

# Base canvas attrs. Aligns to HyperPixel square display
WIDTH = 720
HEIGHT = 720
MARGIN = 25

# Attrs to account for the restricted visible area imposed by 50mm cube
VISIBLE_WIDTH = 550 
VISIBLE_HEIGHT = 550
VISIBLE_OFFSET_X = (WIDTH - VISIBLE_WIDTH) // 2
VISIBLE_OFFSET_Y = (HEIGHT - VISIBLE_HEIGHT) // 2

scene = AquariumScene(width=VISIBLE_WIDTH, height=VISIBLE_HEIGHT, margin=MARGIN)

def settings():
    py5.size(WIDTH,HEIGHT)

def setup():
    """Configures global styling and aquarium artifacts"""
    py5.window_move(0,0) # keep at top-left for intended Pi display
    scene.setup(
        num_fish=5, 
        num_seaweed=10,
        seaweed_spacing=25
    )

def draw():
    """Renders background and manages sea critters"""
    py5.push_matrix()
    py5.translate(VISIBLE_OFFSET_X, VISIBLE_OFFSET_Y)
    
    scene.update()
    scene.display()

    py5.pop_matrix()

py5.run_sketch()
