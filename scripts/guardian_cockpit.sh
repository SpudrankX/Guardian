#!/usr/bin/env bash
# Guardian Unified Cockpit: Phase 11
# Auto-Restart + Combined Logs + Live Status

MANAGER_SCRIPT=~/guardian/modules/manager/guardian_manager_secure.py
HEARTBEAT_SCRIPT=~/guardian/modules/heartbeat/guardian_heartbeat.py
WATCHER_SCRIPT=~/guardian/modules/watcher/guardian_watcher.py

MANAGER_PORT=5095
HEARTBEAT_PORT=5060
WATCHER_PORT=5050

API_TOKEN=RXSECURETOKEN123
SLEEP_INTERVAL=15

echo "[🟢] Launching Guardian Unified Cockpit..."
echo "[💡] Press CTRL+C to exit at any time."

# Function to restart a module if down
check_and_restart() {
    local name=$1
    local port=$2
    local script=$3
    local token=$4

    if [[ $name == "Manager" ]]; then
        if ! curl -H "X-API-TOKEN: $token" -s http://127.0.0.1:$port/status > /dev/null; then
            echo "[🚦] $name down, restarting..."
            pkill -f guardian_manager_secure.py
            python3 $script &
            sleep 2
            echo "[🚦] $name restarted."
        fi
    else
        if ! curl -s http://127.0.0.1:$port/status > /dev/null; then
            echo "[💓] $name down, restarting..."
            pkill -f $(basename $script)
            python3 $script &
            sleep 2
            echo "[💓] $name restarted."
        fi
    fi
}

# Launch logs in background
mkdir -p ~/logs/guardian_combined
LOG_FILE=~/logs/guardian_combined/unified.log
echo "[📄] Combined logs at $LOG_FILE"
touch $LOG_FILE

# Start tailing logs in background
tail -n 20 -f ~/logs/guardian/manager.log ~/logs/heartbeat/heartbeat.log ~/logs/watcher/watcher.log >> $LOG_FILE &
TAIL_PID=$!

# Main monitoring loop
while true; do
    check_and_restart "Manager" $MANAGER_PORT $MANAGER_SCRIPT $API_TOKEN
    check_and_restart "Heartbeat" $HEARTBEAT_PORT $HEARTBEAT_SCRIPT
    check_and_restart "Watcher" $WATCHER_PORT $WATCHER_SCRIPT

    # Display live status
    echo "[$(date +'%H:%M:%S')] Checking Guardian Status..."
    curl -s -H "X-API-TOKEN: $API_TOKEN" http://127.0.0.1:$MANAGER_PORT/status | jq .
    curl -s http://127.0.0.1:$HEARTBEAT_PORT/status | jq .
    curl -s http://127.0.0.1:$WATCHER_PORT/status | jq .

    sleep $SLEEP_INTERVAL
done

# Cleanup on exit
trap "kill $TAIL_PID" EXIT
