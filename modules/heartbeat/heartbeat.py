#!/usr/bin/env python3
import time, datetime, json

logfile = "/data/data/com.termux/files/home/logs/heartbeat/heartbeat.log"
while True:
    with open(logfile, "a") as f:
        f.write(f"[Heartbeat] ping {datetime.datetime.utcnow().isoformat()}\n")
    time.sleep(30)
