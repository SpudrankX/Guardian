#!/usr/bin/env python3
"""
Guardian Heartbeat v6.1
Phase 7: Live heartbeat module fetching configuration from Config API
"""

import time, json, datetime, os, requests
from flask import Flask, jsonify

app = Flask(__name__)
STATUS = {"heartbeat": "initializing", "last_pulse": None, "pid": os.getpid()}

CONFIG_API = "http://127.0.0.1:5090/config"

def load_config():
    try:
        response = requests.get(CONFIG_API, timeout=2)
        return response.json()
    except Exception as e:
        print(f"[!] Failed to load config, using defaults: {e}")
        return {
            "heartbeat_port": 5060,
            "manager_port": 5070,
            "watcher_port": 5050,
            "check_interval": 30
        }

@app.route('/pulse')
def pulse():
    STATUS["last_pulse"] = str(datetime.datetime.utcnow())
    STATUS["heartbeat"] = "alive"
    return jsonify(STATUS)

@app.route('/status')
def status():
    return jsonify(STATUS)

if __name__ == '__main__':
    config = load_config()
    port = config.get("heartbeat_port", 5060)
    STATUS["heartbeat"] = "running"
    print(f"[💓] Guardian Heartbeat v6.1 running on port {port}")
    app.run(host="127.0.0.1", port=port)
