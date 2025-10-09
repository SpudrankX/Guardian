#!/usr/bin/env python3
"""
Guardian Manager v7.0
Phase 9: Security + Self-Update
"""

import os, time, json, datetime, requests, shutil, subprocess
from flask import Flask, jsonify, request, abort

app = Flask("guardian_manager_secure")

CONFIG_API = "http://127.0.0.1:5090/config"
UPDATE_URL = "http://127.0.0.1:5090/latest_manager.py"  # replace with your actual update URL
API_TOKEN = "RXSECURETOKEN123"  # simple auth token for endpoints

STATUS = {
    "guardian": {"status": "running", "pid": os.getpid(), "last_change": str(datetime.datetime.utcnow())},
    "heartbeat": {"status": "unknown", "pid": None, "last_change": None},
}

def load_config():
    try:
        cfg = requests.get(CONFIG_API, timeout=2).json()
        return cfg
    except Exception as e:
        print(f"[!] Failed to load config: {e}")
        return {
            "manager_port": 5095,
            "watcher_port": 5050,
            "heartbeat_port": 5060,
            "check_interval": 30
        }

def check_for_update():
    try:
        response = requests.get(UPDATE_URL, timeout=2)
        if response.status_code == 200:
            local_file = os.path.abspath(__file__)
            with open(local_file, 'w') as f:
                f.write(response.text)
            print("[🔄] Manager updated successfully. Restarting...")
            subprocess.Popen(["python3", local_file])
            exit(0)
    except Exception as e:
        print(f"[!] Update check failed: {e}")

@app.before_request
def require_token():
    token = request.headers.get("X-API-TOKEN")
    if token != API_TOKEN:
        abort(401, description="Unauthorized")

@app.route("/status")
def status():
    STATUS["manager_time"] = str(datetime.datetime.utcnow())
    return jsonify(STATUS)

@app.route("/update")
def update():
    check_for_update()
    return jsonify({"update": "complete"})

if __name__ == "__main__":
    config = load_config()
    port = int(config.get("manager_port", 5095))
    print(f"[🚦] Guardian Manager Secure v7.0 starting on port {port}")
    app.run(host="127.0.0.1", port=port)
