import os
import hmac
import threading
import subprocess

from bottle import Bottle, request, response
import json

app = Bottle()

# device repo root from this file's location so controller works
#  regardless of where the repo is cloned on the Pi
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# X display configs, injected into the sketch subprocess since 
# controller runs outside the graphical desktop environment
DISPLAY_ENV = os.environ.get("DISPLAY", ":0") # use primary display
XAUTHORITY =  os.environ.get("XAUTHORITY", os.path.expanduser("~/.Xauthority")) # holds session's auth cookie

# injected via systemd service file
API_TOKEN = os.environ.get("OPENGHOST_TOKEN", "")
if not API_TOKEN:
    raise RuntimeError("Auth token not set. Refusing to start without auth")

# Registry of valid sketch names as entry points to scripts
SKETCHES = { 
    "aquarium": "aquarium.py"
}

_sketch_process: subprocess.Popen | None = None # used to run sketches via bash

def _authorized() -> bool:
    """Validate request token using constant-time comparison"""
    incoming = request.headers.get('X-API-Token', "")
    return hmac.compare_digest(incoming, API_TOKEN)

def _is_running() -> bool:
    """
    Return True if sketch process exists and has not exited

    Popen.poll() returns None while process is still running
    """
    return _sketch_process is not None and _sketch_process.poll() is None

def _json(data: dict, status_code: int=200) -> str:
    """Sets response content-type and status code, then returns JSON string"""
    response.content_type = 'application/json'
    response.status = status_code

    return json.dumps(data)

@app.route("/start/<sketch_name>", method="POST")
def start(sketch_name: str) -> str:
    """
    Start a sketch on the OpenGhost machine

    Args:
        sketch_name: Name of sketch to execute. Value must match controller registry
    """
    global _sketch_process

    # Check auth and valid input
    if not _authorized():
        return _json({"error": "unauthorized"}, 401)
    
    script = SKETCHES.get(sketch_name)
    if script is None:
        return _json({ "error": "unknown_sketch" }, 404)
    
    if _is_running():
        return _json({"status": "already_running", "pid": _sketch_process.pid})
    
    # Execute subprocess to execute sketch on OpenGhost machine
    env = os.environ.copy()
    env["DISPLAY"] = DISPLAY_ENV
    env["XAUTHORITY"] = XAUTHORITY

    _sketch_process = subprocess.Popen(
        ["bash", "-c", f"source .venv/bin/activate && python {script}"],
        cwd=BASE_DIR,
        env=env
    )
    return _json({"status": "started", "pid": _sketch_process.pid})

@app.route('/stop', method="POST")
def stop() -> str:
    """Stops currently running sketch on OpenGhost machine"""
    global _sketch_process

    if not _authorized():
        return _json({"error": "unauthorized"}, 401)
    
    if not _is_running():
        return _json({"status": "not_running"})
    
    # SIGTERM asks py5 to shut down cleanly. Runs SIGKILL after 5 seconds
    _sketch_process.terminate()
    try:
        _sketch_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        _sketch_process.kill()
    
    _sketch_process = None
    return _json({"status": "stopped"})

@app.route('/shutdown', method="POST")
def shutdown() -> str:
    """Powers off OpenGhost machine using poweroff command."""
    if not _authorized():
        return _json({"error": "unauthorized"}, 401)

    # Two-second delay gives HTTP response time to reach client before network stack goes down
    threading.Timer(2.0, lambda: subprocess.run(["sudo", "/usr/sbin/poweroff"])).start()
    return _json({"status": "shutting_down"})

@app.route('/status')
def status() -> str:
    """Provides current status of controller API"""
    response.content_type = 'application/json'
    pid = _sketch_process.pid if _is_running() else None
    
    return _json({"running": _is_running(), "pid": pid })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
