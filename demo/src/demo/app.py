"""
Demo for TML
"""

import pathlib

import toga
import toga_tml

class Demo(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        tml_path = pathlib.Path(__file__).parent / "ui.xml"
        self.main_window.content = toga_tml.load(tml_path, self=self)
        self.main_window.show()
    def say_hello(self, widget):
        print(f"Hello, {self.name_input.value}")


def main():
    return Demo()