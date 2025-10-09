#!/usr/bin/env bash
# Guardian Auto-Restart + Logs Monitor
# Phase 10: Resilient Guardian Stack

MANAGER_SCRIPT=~/guardian/modules/manager/guardian_manager_secure.py
HEARTBEAT_SCRIPT=~/guardian/modules/heartbeat/guardian_heartbeat.py
WATCHER_SCRIPT=~/guardian/modules/watcher/guardian_watcher.py

MANAGER_PORT=5095
HEARTBEAT_PORT=5060
WATCHER_PORT=5050

API_TOKEN=RXSECURETOKEN123

echo "[🟢] Starting Guardian Auto-Restart Monitor..."

while true; do
    # Check Manager
    if ! curl -H "X-API-TOKEN: $API_TOKEN" -s http://127.0.0.1:$MANAGER_PORT/status > /dev/null; then
        echo "[🚦] Manager down, restarting..."
        pkill -f guardian_manager_secure.py
        python3 $MANAGER_SCRIPT &
        sleep 2
        echo "[🚦] Manager restarted."
    fi

    # Check Heartbeat
    if ! curl -s http://127.0.0.1:$HEARTBEAT_PORT/status > /dev/null; then
        echo "[💓] Heartbeat down, restarting..."
        pkill -f guardian_heartbeat.py
        python3 $HEARTBEAT_SCRIPT &
        sleep 2
        echo "[💓] Heartbeat restarted."
    fi

    # Check Watcher
    if ! curl -s http://127.0.0.1:$WATCHER_PORT/status > /dev/null; then
        echo "[👁️] Watcher down, restarting..."
        pkill -f guardian_watcher.py
        python3 $WATCHER_SCRIPT &
        sleep 2
        echo "[👁️] Watcher restarted."
    fi

    # Sleep for 15 seconds before next check
    sleep 15
done
