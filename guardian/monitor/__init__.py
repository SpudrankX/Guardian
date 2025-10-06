import time, os

LOG_PATH = os.path.expanduser("~/.guardian/logs")
os.makedirs(LOG_PATH, exist_ok=True)

def log_event(event):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(f"{LOG_PATH}/activity.log", "a") as log:
        log.write(f"[{ts}] {event}\n")
