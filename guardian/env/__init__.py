import platform, os

def detect_environment():
    os_type = platform.system()
    arch = platform.machine()
    termux = "com.termux" in os.getenv("PREFIX", "")
    return {
        "os": os_type,
        "arch": arch,
        "termux": termux
    }
