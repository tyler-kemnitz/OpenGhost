# OpenGhost

This is the repository for OpenGhost, an open-source Pepper's Ghost display that uses a Raspberry Pi 5 with a camera, square screen, and a beam splitter cube as the transparent reflector, which sits on top of the screen. 
Additional peripherals, such as microphones, speakers, etc., can be added for some more interactivity via the USB ports.

OpenGhost intends to be a futuristic and aesthetic display medium that can run all sorts of visual and interactive programs, so feel free to get creative by adding your own scripts or modifying the hardware/designs!

| ![Lorenz Attractor on 50 mm](assets/open_ghost_50_mm.jpg) | ![Lorenz Attractor on 70 mm](assets/open_ghost_70_mm.jpg) |
| --- | --- |
| 50 mm beam splitter cube | 70 mm beam splitter cube |

## Setup And Installation

### Hardware
- Raspberry Pi 5 (other versions should work, but the software installation may differ) + Micro SD card
- [HyperPixel 4.0 Square - Hi-Res Display for Raspberry Pi (touchscreen version)](https://shop.pimoroni.com/products/hyperpixel-4-square?variant=30138251444307). 
  - Also found at retailers like Micro Center.
  - Any 4-inch square screen that can attach to the Raspberry Pi 5 pins should work as well
- [70 mm beam splitter cube](https://www.aliexpress.com/item/1005005127247262.html?spm=a2g0o.order_list.order_list_main.17.2d60180247Uidc) or [50 mm beam splitter cube](https://www.aliexpress.com/item/1005006772844723.html?spm=a2g0o.order_list.order_list_main.5.2d60180247Uidc) (I got them off Aliexpress)
- 5V 5A USB-C power supply (5V 3A is suitable as well, but the former is recommended)
- 4x M2.5x14 mm screws
- 3D printed STL files in `/stl_files`
- Camera (optional). The one shown is the [Raspberry Pi Camera Module 3](https://www.raspberrypi.com/products/camera-module-3/)

### Software
I'm using the Python library [py5](https://py5coding.org/index.html) to display graphics. If you are planning to do the same, follow these instructions:

- Install Raspberry Pi OS Bookworm (uses Python 3.11)
  - If using Raspberry Pi Imager, select Legacy 64-bit that specifies Bookworm
- Enable the square display on the Pi by following [these instructions](https://shop.pimoroni.com/products/hyperpixel-4-square?variant=30138251444307). If you used a different display, follow the manufacturer's instructions to enable it
  - For the HyperPixel display, more detailed guidance can be found [here](https://github.com/pimoroni/hyperpixel4/issues/177) 
- Install a virtual environment with system site packages `python -m venv .venv --system-site-packages`
- Install Java headless using `sudo apt update && sudo apt install default-jdk`
  - For Bookworm, this will install Java 17 by default.
- Install py5 using `pip install py5` (requires Java 17+)
- Clone this repo

#### If The Camera Is Being Used
- Downgrade numpy to `numpy==1.26.4` (any numpy version less than 2.0)
- Install dependency `sudo apt install libcap-dev`
- Install picamera2 using `pip install picamera2`
- Install libcamera `sudo apt install libcamera-apps python3-libcamera python3-picamera2`

## How To Run Programs
- Open a terminal and activate the virtual environment
- Run `export DISPLAY=:0.0` if the terminal session is new
- Run the desired Python file

## Alternative Development Workflows

While working on the actual `py5` programs, I found it a bit easier to use my home desktop environment for development.

Through this approach, a couple of the setup steps looked a little different, documented below.
- **OS**: I run Fedora 43 KDE Plasma.
- **Python version**: Although I could (should?) have opted to install and use the same Python version as my Bookworm OS, I opted to use the default v3.14 that came with Fedora.
- **Java Install**: By default, Fedora 43 came with Java 25, which caused py5 installation issues related to JPype and other dependencies. Instead, I opted to use version 21:
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

