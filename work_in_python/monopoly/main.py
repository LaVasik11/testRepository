import threading
import time
import subprocess
import socket
import platform
import shutil
import os
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer
from playwright.sync_api import sync_playwright
from start import ui_loop_step, handle_ws
from GameState import GameState


ui_state = {
    "page": None,
    "started": False,
    "initializing": False
}

game_state = GameState()


def get_chrome_path():
    system = platform.system()

    if system == "Linux":
        return (
            shutil.which("google-chrome") or
            shutil.which("chromium") or
            shutil.which("chromium-browser")
        )

    if system == "Windows":
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]

        for p in paths:
            if os.path.exists(p):
                return p

        return None

    raise RuntimeError("Unsupported OS")


def wait_for_port(port, host="127.0.0.1", timeout=10.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except:
            time.sleep(0.5)
    return False


class BotUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Monopoly Bot")
        self.setFixedSize(300, 200)

        self.layout = QVBoxLayout()

        self.status = QLabel("Status: OFF")
        self.layout.addWidget(self.status)

        self.init_btn = QPushButton("Init Browser")
        self.init_btn.clicked.connect(self.start_init)
        self.layout.addWidget(self.init_btn)

        self.loop_btn = QPushButton("Start")
        self.loop_btn.clicked.connect(self.toggle_loop)
        self.loop_btn.setEnabled(False)
        self.layout.addWidget(self.loop_btn)

        self.setLayout(self.layout)

        self.chrome_proc = None
        self.loop_event = threading.Event()

        self.monitor = QTimer()
        self.monitor.timeout.connect(self.check_browser)
        self.monitor.start(500)

    def start_init(self):
        self.init_btn.hide()
        threading.Thread(target=self.worker, daemon=True).start()

    def toggle_loop(self):
        if not ui_state["started"]:
            return

        if self.loop_event.is_set():
            self.loop_event.clear()
            self.loop_btn.setText("Start")
            self.status.setText("Status: PAUSED")
        else:
            self.loop_event.set()
            self.loop_btn.setText("Stop")
            self.status.setText("Status: RUNNING")

    def check_browser(self):
        if self.chrome_proc and self.chrome_proc.poll() is not None:
            self.cleanup_after_close()

    def cleanup_after_close(self):
        ui_state["started"] = False

        self.loop_event.clear()

        self.loop_btn.setText("Start")
        self.loop_btn.setEnabled(False)

        self.init_btn.show()
        self.status.setText("Status: OFF")

        self.chrome_proc = None

    def worker(self):
        ui_state["initializing"] = True

        chrome_path = get_chrome_path()
        if not chrome_path:
            self.status.setText("Chrome not found")
            ui_state["initializing"] = False
            self.init_btn.show()
            return

        user_data_dir = (
            r"C:\temp\chrome-profile"
            if platform.system() == "Windows"
            else "/tmp/chrome-profile"
        )

        self.chrome_proc = subprocess.Popen([
            chrome_path,
            "--remote-debugging-port=9222",
            f"--user-data-dir={user_data_dir}"
        ])

        if not wait_for_port(9222):
            self.status.setText("Chrome failed")
            ui_state["initializing"] = False
            self.init_btn.show()
            return

        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")

            context = browser.contexts[0]
            page = context.pages[0]

            page.on("websocket", lambda ws: handle_ws(ws, game_state))
            page.goto("https://monopoly-one.com/games")

            ui_state["page"] = page
            ui_state["started"] = True
            ui_state["initializing"] = False

            self.status.setText("Status: READY")
            self.loop_btn.setEnabled(True)

            while True:
                if self.chrome_proc and self.chrome_proc.poll() is not None:
                    self.cleanup_after_close()
                    break

                if self.loop_event.is_set():
                    ui_loop_step(page, game_state)
                    time.sleep(0.2)
                else:
                    time.sleep(0.1)


if __name__ == "__main__":
    app = QApplication([])

    window = BotUI()
    window.show()

    app.exec()