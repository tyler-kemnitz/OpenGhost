import os
import hmac
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

# Registry of valid sketch names as entry points to scripts
SKETCHES = { 
    "aquarium": "aquraium.py"
}

_process: subprocess.Popen | None = None # used to run sketches via bash

def _authorized() -> bool:
    """Validate request token using constant-time comparison"""
    incoming = request.headers.get('X-API-Token', "")
    return hmac.compare_digest(incoming, API_TOKEN)

def _is_running() -> bool:
    """
    Return True if sketch process exists and has not exited

    Popen.poll() returns None while process is still running
    """
    return _process is not None and _process.poll() is None

def _json(data: dict, status: int=200) -> str:
    """Sets response content-type and status code, then returns JSON string"""
    response.content_type = 'application/json'
    response.status = status

    return json.dumps(data)

def _validate() -> str | None:
    return None # TODO::Consolidate auth and is_running checks here

@app.route("/start/<sketch_name>")
def start(sketch_name: str) -> str:
    global _process

    if not _authorized():
        return _json({"error": "unauthorized"}, 401)
    
    script = SKETCHES.get(sketch_name)
    if script is None:
        return _json({ "error": "unknown_sketch" }, 404)
    
    if _is_running():
        return _json({"status": "already_running", "pid": _process.pid})
    
    env = os.environ.copy()
    env["DISPLAY"] = DISPLAY_ENV
    env["XAUTHORITY"] = XAUTHORITY

    _process = subprocess.Popen(
        ["bash", "-c", f"source .venv/bin/activate && python {script}"],
        cwd=BASE_DIR,
        env=env
    )
    return _json({"status": "started", "pid": _process.pid})

@app.route('/stop')
def stop() -> str:
    global _process

    if not _authorized():
        return _json({"error": "unauthorized"}, 401)
    
    if not _is_running():
        return _json({"status": "not_running"})
    
    # SIGTERM asks py5 to shut down cleanly. Runs SIGKILL after 5 seconds
    _process.terminate()
    try:
        _process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        _process.kill()
    
    _process = None
    return _json({"status": "stopped"})

@app.route('/status')
def status() -> str:
    response.content_type = 'application/json'
    pid = _process.pid if _is_running() else None
    
    return _json({"running": _is_running(), "pid": pid })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
