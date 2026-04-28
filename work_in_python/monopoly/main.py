import subprocess
import time
import socket
import platform
import shutil
import sys


def wait_for_port(port, host="127.0.0.1", timeout=10.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except:
            time.sleep(0.5)
    return False


def get_chrome_command():
    system = platform.system()

    if system == "Linux":
        return shutil.which("chromium-browser") or shutil.which("chromium") or shutil.which("google-chrome")

    if system == "Windows":
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        for path in possible_paths:
            try:
                with open(path):
                    return path
            except:
                continue

    raise RuntimeError("Chrome/Chromium not found")


chrome_path = get_chrome_command()

chromium_cmd = [
    chrome_path,
    "--remote-debugging-port=9222",
    "--user-data-dir=/tmp/chrome-profile"
]

subprocess.Popen(chromium_cmd)

if not wait_for_port(9222):
    raise RuntimeError("Chrome did not start")

subprocess.run([sys.executable, "start.py"])