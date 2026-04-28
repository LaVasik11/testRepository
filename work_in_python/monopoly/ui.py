import threading
import time
import subprocess
import socket
import platform
import shutil

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel

from playwright.sync_api import sync_playwright

from start import ui_loop_step, handle_ws
from GameState import GameState


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

    raise RuntimeError("Chrome not found")


ui_state = {
    "page": None,
    "started": False,
    "loop_running": False,
    "initializing": False
}

game_state = GameState()


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

        self.loop_running = False

    def start_init(self):
        self.init_btn.hide()
        threading.Thread(target=self.worker, daemon=True).start()

    def toggle_loop(self):
        if not ui_state["started"]:
            return

        self.loop_running = not self.loop_running
        ui_state["loop_running"] = self.loop_running

        if self.loop_running:
            self.loop_btn.setText("Stop")
            self.status.setText("Status: RUNNING")
        else:
            self.loop_btn.setText("Start")
            self.status.setText("Status: PAUSED")

    def worker(self):
        ui_state["initializing"] = True

        chrome_path = get_chrome_command()

        subprocess.Popen([
            chrome_path,
            "--remote-debugging-port=9222",
            "--user-data-dir=/tmp/chrome-profile"
        ])

        if not wait_for_port(9222):
            self.status.setText("Chrome failed")
            ui_state["initializing"] = False
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
                if ui_state["loop_running"]:
                    ui_loop_step(page, game_state)
                    time.sleep(0.2)
                else:
                    time.sleep(0.1)


if __name__ == "__main__":
    app = QApplication([])

    window = BotUI()
    window.show()

    app.exec()