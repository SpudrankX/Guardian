#!/usr/bin/env python3
"""
Guardian Manager (Phase 6)
Now dynamically loads configuration from guardian_config API.
"""

import os, time, json, datetime, requests
from flask import Flask, jsonify

app = Flask("guardian_manager")

CONFIG_URL = "http://127.0.0.1:5090/config"

def load_config():
    try:
        cfg = requests.get(CONFIG_URL, timeout=2).json()
        print(f"[⚙️] Loaded configuration v{cfg.get('version')} at {cfg.get('updated')}")
        return cfg
    except Exception as e:
        print(f"[!] Could not fetch config: {e}")
        # fallback defaults
        return {
            "manager_port": 5070,
            "watcher_port": 5050,
            "heartbeat_port": 5060,
            "check_interval": 30
        }

config = load_config()
STATUS = {
    "guardian": {"status": "running", "pid": os.getpid(), "last_change": str(datetime.datetime.utcnow())},
    "heartbeat": {"status": "unknown", "pid": None, "last_change": None},
}

@app.route("/status")
def status():
    STATUS["guardian"]["last_change"] = str(datetime.datetime.utcnow())
    return jsonify({
        "guardian": STATUS["guardian"],
        "heartbeat": STATUS["heartbeat"],
        "manager_time": str(datetime.datetime.utcnow())
    })

if __name__ == "__main__":
    port = int(config.get("manager_port", 5070))
    print(f"[🚦] Guardian Manager v6.0 starting on port {port}")
    app.run(host="127.0.0.1", port=port)
