# OpenGhost

This is the repository for OpenGhost, an open-source [Pepper's Ghost](https://en.wikipedia.org/wiki/Pepper%27s_ghost) display that uses a Raspberry Pi 5 with a camera, square screen, and a beam splitter cube as the transparent reflector, which sits on top of the screen. 
Additional peripherals, such as microphones, speakers, etc., can be added for some more interactivity via the USB ports.

OpenGhost intends to be a futuristic and aesthetic display medium that can run all sorts of visual and interactive programs, so feel free to get creative by adding your own scripts or modifying the hardware/designs!

| ![Lorenz Attractor on 50 mm](assets/open_ghost_50_mm.jpg) | ![Lorenz Attractor on 70 mm](assets/open_ghost_70_mm.jpg) |
|-----------------------------------------------------------|-----------------------------------------------------------|
| 50 mm beam splitter cube                                  | 70 mm beam splitter cube                                  |

## Table of Contents
- [Setup And Installation](#setup-and-installation)
- [Project Structure](#project-structure)
- [How To Run Programs](#how-to-run-programs)
- [Alternative Development Workflows](#alternative-development-workflows)

## Setup And Installation

### Hardware
- Raspberry Pi 5 (other versions should work, but the software installation may differ) + Micro SD card
- [HyperPixel 4.0 Square - Hi-Res Display for Raspberry Pi (touchscreen version)](https://shop.pimoroni.com/products/hyperpixel-4-square?variant=30138251444307). 
  - May be found at retailers like Micro Center.
  - Any 4-inch square screen that can attach to the Raspberry Pi 5 pins should work as well
- [70 mm beam splitter cube](https://www.aliexpress.com/item/1005005127247262.html?spm=a2g0o.order_list.order_list_main.17.2d60180247Uidc) or [50 mm beam splitter cube](https://www.aliexpress.com/item/1005006772844723.html?spm=a2g0o.order_list.order_list_main.5.2d60180247Uidc) (I got them off Aliexpress)
- 5V 5A USB-C power supply (5V 3A is suitable as well, but the former is recommended)
- 4x M2.5x14 mm screws
- 3D printed STL files in `/stl_files`
- Camera (optional). The one shown is the [Raspberry Pi Camera Module 3](https://www.raspberrypi.com/products/camera-module-3/)

### Software
I'm using the Python library [py5](https://py5coding.org/index.html) to display graphics, and a small [Bottle](https://bottlepy.org/docs/dev/) HTTP service for remote execution on the Pi.

1.  Install Raspberry Pi OS Bookworm (uses Python 3.11)
    1.  If using Raspberry Pi Imager, it will likely be a Legacy 64-bit install that specifies Bookworm
2. Enable the square display on the Pi by following [these instructions](https://shop.pimoroni.com/products/hyperpixel-4-square?variant=30138251444307). If you used a different display, follow the manufacturer's instructions to enable it
    1. For the HyperPixel display, more detailed guidance can be found [here](https://github.com/pimoroni/hyperpixel4/issues/177)
3. Install Java using `sudo apt update && sudo apt install default-jdk`. Ensure you install **version 17 or higher**.
   1. For Bookworm, this will install Java 17 by default.
4. Clone this repository and `cd` into the base directory.
5. Install a virtual environment with system site packages: `python -m venv .venv --system-site-packages`
6. Activate the virtual environment: `source .venv/bin/activate`
7. Install Python dependencies: `pip install -r requirements.txt`

> **Note**: Bookworm's Wayland compositor requires additional one-time configuration before sketches will render correctly. See [```docs/labwc-configuration.md```](docs/labwc-configuration.md).

#### If The Camera Is Being Used
- Downgrade numpy to `numpy==1.26.4` (any numpy version less than 2.0)
- Install dependency `sudo apt install libcap-dev`
- Install picamera2 using `pip install picamera2`
- Install libcamera `sudo apt install libcamera-apps python3-libcamera python3-picamera2`

## Project Structure

As OpenGhost programs grow more complex, the repo separates a few concerns so any single file stays easy to read:

- **Entry-point scripts** (e.g. `aquarium.py`) live at the repo root. These are the files you actually run with `python <file>.py`. They should stay thin and only implement the three functions py5 requires: `settings()`, `setup()`, and `draw()` — all delegating to a scene.
- **`scenes/`** holds `Scene` classes that own and orchestrate everything an entry-point script draws (e.g. `AquariumScene`). A scene exposes `setup()`, `update()`, and `display()`, following the contract in `scenes/scene.py`, so an entry-point script stays simple no matter how many entities the scene manages.
- **`entities/`** holds the drawable object classes themselves (e.g. `Fish`, `Seaweed`). Each entity knows how to update and draw itself, but nothing about what else exists in the scene around it.
- **`common/`** holds small, reusable helpers shared across entities or scenes that aren't tied to any one entity (angle math, font setup, etc.).
- **`debug/`** is reserved for standalone scripts used to debug or visualize a sketch (an FPS overlay, a margin visualizer, etc.). These are dev tools, not part of any production sketch.
- **`controller/`** holds the Bottle-based HTTP control server that allows remote control of sketches from other devices on the local network.


> To add a new sketch: 
> 1. Create a Scene class under `scenes/`, 
> 2. Add any new drawable entities under `entities/`, and render them within your new scene.
> 3. Add an entry-point script at the repo root that wires the scene into py5's lifecycle, following the pattern in `aquarium.py`.
> 4. Register the new entry-point script in the `SKETCHES` dict in `controller/controller.py`.
> 5. Restart the controller service on the Pi (see *Remote Execution* below)

## How To Run Programs

### Local Execution
Better for early prototyping and setup. If you're doing testing on a non-Pi machine, simply set up your bash environment and run your sketch from the repo's base directory:
1. Set up venv and display config: `source prep_env.sh`
2. Run the desired entry-point script: `python sketch.py`

### Remote Execution
Once the Pi's controller service is running, sketches can be started and stopped from any device on the same network. 

See [docs/remote-controller.md](docs/remote-controller.md) for full setup instructions.
 
Once configured, verify a sketch is registered and reachable from any machine on the network:
```bash
curl -X POST -H "X-API-Token: <token>" http://<pi-ip>:5000/start/<sketch_name>
```

## Alternative Development Workflows

While working on the actual `py5` programs, I found it a bit easier to use my home desktop environments for development and testing rather than running everything on the Pi.

Through this approach, a couple of the setup steps looked a little different depending on the OS. Most of the nuance exists in dependency version management. Whatever you choose, be sure to stay as close to your Bookworm configuration as you can.

- **OS**: I was mostly running Fedora 43 KDE Plasma. 
  - I also had a Mac running Sequoia 15.6. Check out py5's [Mac-specific documentation](https://py5coding.org/content/macos_users.html) if you run into issues.
- **Python version**: Although I could (should?) have opted to install and use the same Python version as my Bookworm OS, I opted to use the default v3.14 that came with my other machines.
- **Java Install (Linux)**: By default, Fedora 43 came with Java 25, which caused py5 installation issues related to JPype and other dependencies. Instead, I opted to use version 21:
  - Install version 21: `sudo dnf install java-21-openjdk`
  - Use `sudo alternatives --config java` to use version 21.
  - If you still run into issues, consider configuring `PATH` with `JAVA_HOME` in your `.bashrc`:
    ```
        export JAVA_HOME="usr/lib/jvm/java-21-openjdk"
        if ! [[ "$PATH" =~ "$JAVA_HOME/bin" ]]; then
          PATH="JAVA_HOME/bin:$PATH"
        fi
      
        export PATH
    ```
