# -- Module --
from pynput.mouse import Button
from pynput import keyboard
from .click_class import *

# -- Default value --
check_autoclick = {"left":False, "right":False}
button = {"right": Button.right, "left": Button.left}
check_click = {"left":False, "right":False}

# -- Main class --
class AutoClick:
    def __init__(self, right_key="v", left_key="x", delay=0.04):
        self.cps = delay
        self.key = {"right": right_key, "left": left_key}
        self.right_click = Click(self.cps, button["right"])
        self.right_click.start()
        self.left_click = Click(self.cps, button["left"])
        self.left_click.start()

    def set_autoclick_key(self, right_key, left_key):
        self.key["right"] = right_key
        self.key["left"] = left_key
    
    def run_autoclick_right(self):
        if check_autoclick["right"]:
            check_autoclick["right"] = False
            self.right_click.start_clicker()
        else:
            check_autoclick["right"] = True
            self.right_click.stop_clicker()

    def run_autoclick_left(self):
        if check_autoclick["left"]:
            check_autoclick["left"] = False
            self.left_click.start_clicker()
        else:
            check_autoclick["left"] = True
            self.left_click.stop_clicker()

    def run_autoclick(self):
        if self.key["right"] != None and self.key["left"] != None:
            with keyboard.GlobalHotKeys({
                str(self.key["right"]): self.run_autoclick_right,
                str(self.key["left"]): self.run_autoclick_left}) as h:
                h.join()
        else:
            raise ValueError("key right or key left is NoneType!")