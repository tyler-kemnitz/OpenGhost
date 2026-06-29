# Remote Controller Setup
OpenGhost includes a lightweight HTTP control server (`controller/controller.py`) that lets you start and stop sketches remotely from any device on the same network. In this way, you can set up RESTful clients to manage your machine.

The following steps will guide you through creating a `systemd` service on the Pi that exposes `controller.py` as an authenticated API to other devices on the same network.

1. Generate secret token: `python -c "import secrets; print(secrets.token_hex(32))"`
  1. Copy the output for use in the next two steps.
2. Create the `.env` file the service will use to store the token:
```bash
mkdir -p ~/.config/systemd/user
touch ~/.config/systemd/user/openghost.env
chmod 600 ~/.config/systemd/user/openghost.env
```
Add the following line to `openghost.env`, substituting your generated token:
```
OPENGHOST_TOKEN=your_generated_token_here
```
3. **Create the service file** at `~/.config/systemd/user/openghost-controller.service`. Directories under `.config` may need to be created as well.
```ini
[Unit]
Description=OpenGhost HTTP Controller
After=network.target
 
[Service]
Type=simple
WorkingDirectory=/home/<user_path>/OpenGhost
ExecStart=/home/<user_path>/OpenGhost/.venv/bin/python controller/controller.py
EnvironmentFile=/home/<user_path>/.config/systemd/user/openghost.env
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
 
[Install]
WantedBy=default.target
```
  1. Ensure `WorkingDirectory`, `ExecStart`, and `EnvironmentFile` point to the correct locations within the Pi user's files.
4. Enable and start the service:
```bash
loginctl enable-linger <user>
systemctl --user daemon-reload
systemctl --user enable openghost-controller
systemctl --user start openghost-controller
systemctl --user status openghost-controller
```

### Useful Service Commands
```bash
journalctl --user -u openghost-controller -f        # tail live logs while server is running
systemctl --user restart openghost-controller       # after editing controller.py, restart controller
systemctl --user daemon-reload && systemctl --user restart openghost-controller  # after editing the service file, reload entire service
```

> To keep the Pi's address stable, consider assigning a static IP via a DHCP reservation in your router's admin interface.
> Find the Pi's MAC address with `ip link show`. Look for `wlan0` (wireless) or `eth0` (wired) and map it to the fixed address. No port forwarding is needed or recommended.

### Client Example: Apple Shortcuts Setup
Each action requires one Shortcut with a single **Get Contents of URL** action:

| | Start | Stop | Status |
|---|---|---|---|
| **URL** | `http://<pi-ip>:5000/start/aquarium` | `http://<pi-ip>:5000/stop` | `http://<pi-ip>:5000/status` |
| **Method** | POST | POST | GET |
| **Header** | `X-API-Token: <your token>` | `X-API-Token: <your token>` | `X-API-Token: <your token>` |

Add a **Show Result** action after the URL fetch to display the JSON response. For sketch selection, add an **Ask for Input** step before the fetch and interpolate the result into the URL path: `http://<pi-ip>:5000/start/<input>`.