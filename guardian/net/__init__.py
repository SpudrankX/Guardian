import requests

def check_internet():
    try:
        requests.get("https://github.com", timeout=3)
        return True
    except Exception:
        return False
