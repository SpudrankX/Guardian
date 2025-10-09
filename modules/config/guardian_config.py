#!/usr/bin/env python3
"""
Guardian Config Service (Phase 5)
Provides local-only Flask API for reading/writing system configuration.
"""

import os, json
from flask import Flask, jsonify, request
from datetime import datetime

CONFIG_PATH = os.path.expanduser("~/guardian/config/config.json")

# Ensure config file exists with default values
default_config = {
    "version": "5.0",
    "manager_port": 5070,
    "watcher_port": 5050,
    "heartbeat_port": 5060,
    "check_interval": 30,
    "updated": str(datetime.utcnow())
}

os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w") as f:
        json.dump(default_config, f, indent=2)

app = Flask("guardian_config")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(data):
    data["updated"] = str(datetime.utcnow())
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)
    return data

@app.route("/config", methods=["GET"])
def get_config():
    return jsonify(load_config())

@app.route("/config", methods=["POST"])
def update_config():
    incoming = request.get_json(force=True)
    current = load_config()
    current.update(incoming)
    return jsonify(save_config(current))

@app.route("/ping")
def ping():
    return jsonify({"status": "ok", "time": str(datetime.utcnow())})

if __name__ == "__main__":
    print("[⚙️] Guardian Config API running on http://127.0.0.1:5090")
    app.run(host="127.0.0.1", port=5090)
