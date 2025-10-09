#!/usr/bin/env python3
"""
Guardian Watcher v6.0
Phase 8: Links Guardian Manager + Heartbeat
Monitors module status and logs real-time health.
"""

import time, json, datetime, requests, os
from flask import Flask, jsonify

app = Flask(__name__)
STATUS = {
    "active": True,
    "manager_status": None,
    "heartbeat_status": None,
    "time": str(datetime.datetime.utcnow())
}

MANAGER_API = "http://127.0.0.1:5095/status"
HEARTBEAT_API = "http://127.0.0.1:5060/status"
CHECK_INTERVAL = 5  # seconds between checks

def update_status():
    try:
        manager = requests.get(MANAGER_API, timeout=2).json()
        STATUS["manager_status"] = manager["guardian"]["status"]
    except:
        STATUS["manager_status"] = "down"

    try:
        heartbeat = requests.get(HEARTBEAT_API, timeout=2).json()
        STATUS["heartbeat_status"] = heartbeat["heartbeat"]
    except:
        STATUS["heartbeat_status"] = "down"

    STATUS["time"] = str(datetime.datetime.utcnow())

@app.route('/status')
def status():
    update_status()
    return jsonify(STATUS)

if __name__ == '__main__':
    print(f"[👁️] Guardian Watcher v6.0 running, monitoring Manager + Heartbeat")
    app.run(host="127.0.0.1", port=5050)
