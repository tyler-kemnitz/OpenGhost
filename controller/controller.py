import os
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

# Registry of valid sketch names as entry points to scripts
SKETCHES = [
    { "aquarium": "aquraium.py" },
]

_process: subprocess.Popen | None = None # used to run sketches via bash

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

@app.route('/status')
def status() -> str:
    response.content_type = 'application/json'
    pid = _process.pid if _is_running() else None
    
    return _json({"running": _is_running(), "pid": pid })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
