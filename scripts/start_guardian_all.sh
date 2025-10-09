#!/usr/bin/env bash
# Guardian Unified Startup Script
# Phase 7–9: Manager Secure + Heartbeat + Watcher
# --------------------------------------------

echo "[🟢] Starting Guardian Unified Stack..."

# Kill any existing Guardian processes to avoid port conflicts
pkill -f guardian_manager_secure.py
pkill -f guardian_heartbeat.py
pkill -f guardian_watcher.py
sleep 1

# Start Heartbeat (v6.1)
echo "[💓] Starting Heartbeat v6.1..."
python3 ~/guardian/modules/heartbeat/guardian_heartbeat.py &
HEARTBEAT_PID=$!
sleep 2
echo "[💓] Heartbeat started with PID $HEARTBEAT_PID on port 5060"

# Start Manager Secure (v7.0)
echo "[🚦] Starting Manager Secure v7.0..."
python3 ~/guardian/modules/manager/guardian_manager_secure.py &
MANAGER_PID=$!
sleep 2
echo "[🚦] Manager Secure started with PID $MANAGER_PID on port 5095"

# Start Watcher (v6.0)
echo "[👁️] Starting Watcher v6.0..."
python3 ~/guardian/modules/watcher/guardian_watcher.py &
WATCHER_PID=$!
sleep 2
echo "[👁️] Watcher started with PID $WATCHER_PID on port 5050"

# Show live status
echo "[🔎] Checking status..."
curl -H "X-API-TOKEN: RXSECURETOKEN123" -s http://127.0.0.1:5095/status | jq .
curl -s http://127.0.0.1:5060/status | jq .
curl -s http://127.0.0.1:5050/status | jq .

echo "[✅] Guardian Unified Stack is now running!"
