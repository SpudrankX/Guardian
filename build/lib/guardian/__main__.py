import subprocess
import platform
import sys
import os

def get_git_info():
    """Retrieve branch name and last commit message."""
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
        commit_msg = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%s"], stderr=subprocess.DEVNULL
        ).decode().strip()
        return branch, commit_msg
    except Exception:
        return "unknown", "unavailable"

def system_info():
    """Return Python and system information."""
    return {
        "python": platform.python_version(),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "env": os.getenv("PREFIX", "Termux/Linux")
    }

def main():
    branch, commit = get_git_info()
    info = system_info()

    print("Guardian Framework v3.6 — Build Stable")
    print("---------------------------------------")
    print(f"Branch: {branch}")
    print(f"Last Commit: {commit}")
    print(f"Python: {info['python']}")
    print(f"System: {info['system']} {info['release']} ({info['machine']})")
    print(f"Environment: {info['env']}")
    print("Status: ✅ All systems operational\n")

    if "--version" in sys.argv:
        print("Guardian CLI Version: v3.6 — Diagnostic Build")
    elif "--sync" in sys.argv:
        os.system("git sync")
    else:
        print("Ready for next instruction...")

if __name__ == "__main__":
    main()
