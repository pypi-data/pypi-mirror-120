import time
import threading
from pynput.mouse import Button, Controller

class Click(threading.Thread):
    def __init__(self, cps, button):
        super().__init__()
        self.delay = cps
        self.button = button
        self.running = False
        self.progarm_running = True
        self.mouse = Controller()

    def start_clicker(self):
        self.running = True

    def stop_clicker(self):
        self.running = False

    def run(self):
        try:
            while self.progarm_running:
                while self.running:
                    self.mouse.click(self.button)
                    time.sleep(self.delay)
                time.sleep(0.01)
            exit()

        except Exception as e:
            exit()