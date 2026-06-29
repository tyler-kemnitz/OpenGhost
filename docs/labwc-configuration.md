# Configuring labwc for OpenGhost
Bookworm uses `labwc` as its Wayland compositor. By default, `labwc` launches two components on boot that interfere with running OpenGhost sketches full-screen.

- **`wf-panel-pi`**: The desktop taskbar. It reserves a permanent strip of screen space, causing the compositor to shrink any application window (sketches) to avoid overlapping. This will ultimately cause the canvas to render smaller than its intended dimensions.
- **`pacmanfm --desktop`**: *Optional* The desktop background and icon manager. This doesn't directly interfere but is an unnecessary background process for a dedicated display device.

Both are launched at session start by `labwc`'s autostart file. To disable, edit in a text editor (e.g., `nano`):

```bash
sudo nano /etc/xdg/labwc/autostart
```
 
Comment out the relevant lines by adding a `#` at the start:
 
```bash
#/usr/bin/lwrespawn /usr/bin/wf-panel-pi &
#/usr/bin/lwrespawn /usr/bin/pcmanfm --desktop --profile LXDE-pi &
```
 
### Removing Window Decorations
 
By default, labwc adds a title bar and thin border around every window (collectively called server-side decorations). For a py5 sketch running at 720×720, these decorations push the total window footprint beyond the physical display's dimensions, causing horizontal and vertical overflow.
 
To disable decorations globally, edit (or create) `~/.config/labwc/rc.xml`. The root element in this file is `<openbox_config>`. Add the following block just before the closing `</openbox_config>` tag:
 
```xml
<windowRules>
  <windowRule identifier="*" serverDecoration="no" />
</windowRules>
```
 
This tells labwc not to draw any server-side decorations on any window, which is appropriate for a dedicated kiosk display. Reload the config one-time without rebooting using:
 
```bash
killall -s SIGHUP labwc
```
 
After making both changes, py5 sketches will render at the correct dimensions with no OS chrome interfering.