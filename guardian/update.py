import os
import subprocess

def auto_update():
    print("🔄 Checking for updates on Guardian v3.7 ...")
    try:
        subprocess.run(["git", "pull", "origin", "v3.7"], check=True)
        subprocess.run(["pip", "install", ".", "--force-reinstall"], check=True)
        print("✅ Guardian v3.7 updated successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ Update failed:", e)

def check_version():
    print("Guardian v3.7 — Aegis Protocol (Build Active)")
    print("Repo branch: v3.7")

if __name__ == "__main__":
    auto_update()
