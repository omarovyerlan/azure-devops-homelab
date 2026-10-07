"""Small status dashboard used as the demo app for the DevOps home lab."""
import os
import platform
import socket
import time
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template

app = Flask(__name__)

START_TIME = time.time()
APP_VERSION = os.getenv("APP_VERSION", "dev")
ENVIRONMENT = os.getenv("APP_ENV", "local")


def uptime_seconds() -> int:
    return int(time.time() - START_TIME)


def system_info() -> dict:
    return {
        "hostname": socket.gethostname(),
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "python": platform.python_version(),
        "os": f"{platform.system()} {platform.release()}",
        "uptime_seconds": uptime_seconds(),
        "time_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


@app.route("/")
def index():
    return render_template("index.html", info=system_info())


@app.route("/health")
def health():
    """Used by Docker HEALTHCHECK, load balancers and monitoring."""
    return jsonify(status="ok", uptime_seconds=uptime_seconds())


@app.route("/api/info")
def info():
    return jsonify(system_info())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
