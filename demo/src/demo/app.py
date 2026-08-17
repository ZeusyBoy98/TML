"""
Demo for TML
"""

import pathlib
import faker

import toga
import toga_tml

def greeting(name):
    if name:
        return f"Hello, {name}"
    else:
        return "Hello, stranger"

class Demo(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        tml_path = pathlib.Path(__file__).parent / "ui.xml"
        self.main_window.content = toga_tml.load(tml_path, self=self)
        self.main_window.show()
    
    async def say_hello(self, widget):
        fake = faker.Faker()
        await self.main_window.dialog(
            toga.InfoDialog(
                greeting(self.name_input.value),
                f"A message from {fake.name()}: {fake.text()}",
            )
        )


def main():
    return Demo()