import py5

WIDTH = 750
HEIGHT = 750
GRID_SPACING = 50

def settings():
    py5.size(WIDTH, HEIGHT)

def setup():
    py5.text_align(py5.LEFT, py5.TOP)
    py5.text_size(14)

"""Creates 50 px grid for WIDTH x HEIGHT windowed screen
"""
def draw():
    py5.background(0)
    py5.stroke(255)
    py5.stroke_weight(1)

    for x in range(0, WIDTH, GRID_SPACING):
        py5.line(x, 0, x, HEIGHT)
        py5.fill(255)
        py5.text(str(x), x + 2, 2)

    for y in range(0, HEIGHT, GRID_SPACING):
        py5.line(0, y, WIDTH, y)
        py5.fill(255)
        py5.text(str(y), 2, y + 2)

py5.run_sketch()