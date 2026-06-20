import platform
import py5

def get_sys_mono_font() -> str:
    """Determine an appropriate monospace font name for the current OS"""
    fonts = {
        "Linux": "Noto Sans Mono",   # Linux font present on both Fedora and Bookworm
        "Darwin": "Menlo",           # macOS default mono font
        "Windows": "Consolas"        # Obligatory Windows support
    }
    return fonts.get(platform.system(), "Courier New")

def set_mono_font(size: int = 32) -> None:
    """
    Create and apply OpenGhost's default monospace font.

    Must be called from setup() (or later) — py5.create_font() needs an
    active sketch/canvas to load the font against, so calling this at
    import time or before py5.run_sketch() has started will fail.
    """
    mono_font = py5.create_font(get_sys_mono_font(), size)
    py5.text_font(mono_font)
    py5.text_align(py5.LEFT, py5.CENTER)
