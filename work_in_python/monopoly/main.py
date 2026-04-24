import subprocess
import time
import socket


def wait_for_port(port, host="127.0.0.1", timeout=10.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except:
            time.sleep(0.5)
    return False


chromium_cmd = [
    "chromium-browser",
    "--remote-debugging-port=9222",
    "--user-data-dir=/tmp/chrome-profile"
]

subprocess.Popen(chromium_cmd)

if not wait_for_port(9222):
    raise RuntimeError("Chrome did not start")

subprocess.run(["python3", "start.py"])