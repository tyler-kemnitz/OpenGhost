import py5

def draw_frame(width: int, height: int):
    """Draws border of specified dimensions"""
    py5.push_style()

    py5.no_fill()
    py5.stroke(250)
    py5.stroke_weight(3)
    py5.rect(0,0, width, height)

    py5.pop_style()