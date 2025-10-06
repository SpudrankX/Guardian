import sys
from guardian.update import auto_update, check_version
from guardian.env import detect_environment
from guardian.monitor import log_event
from guardian.net import check_internet

def main():
    args = sys.argv[1:]
    if "--version" in args:
        check_version()
    elif "--update" in args:
        auto_update()
    elif "--status" in args:
        env = detect_environment()
        print("🌐 Guardian v3.7 System Status")
        print("OS:", env["os"])
        print("Architecture:", env["arch"])
        print("Termux:", env["termux"])
        print("Internet:", "Online" if check_internet() else "Offline")
    else:
        print("Guardian Framework v3.7 — Aegis Protocol Initialized.")
        print("Use --status | --update | --version")

    log_event(f"Command executed: {' '.join(args) if args else 'default'}")

if __name__ == "__main__":
    main()
