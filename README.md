# TML

<!-- rumdl-disable MD013 -->
[![Python Versions](https://img.shields.io/pypi/pyversions/toga.svg)](https://pypi.python.org/pypi/toga-tml)
[![License](https://img.shields.io/pypi/l/toga-tml)](https://github.com/ZeusyBoy98/TML/blob/main/LICENSE)
[![PyPI Version](https://img.shields.io/pypi/v/toga-tml)](https://pypi.python.org/pypi/toga-tml)
[![Project status](https://img.shields.io/pypi/status/toga-tml)](https://pypi.python.org/pypi/toga-tml)
[![Build Status](https://github.com/ZeusyBoy98/TML/actions/workflows/python-publish.yml/badge.svg)](https://github.com/ZeusyBoy98/TML/actions/workflows/python-publish.yml)
![Repo Size](https://img.shields.io/github/repo-size/ZeusyBoy98/TML)
<!-- rumdl-enable MD013 -->

![TML Logo](https://github.com/ZeusyBoy98/TML/blob/main/logo.png)

## Toga Markup Language
A markup language for the Toga Python framework. Allows you to build cross-platform GUIs in Python, but with an XML tag syntax.

## Why
The Toga framework for Python is really cool. It lets you make cross-platform user interfaces that you can use with BeeWare, and I really want to learn it and use it. When I started using it, I was immediately put off by how it makes the UI. It feels like making a whole website using just the JavaScript DOM. So I had the idea to build a markup language like HTML that I could use with Toga and BeeWare to make development so much easier for myself.

## Requirements
The TML requirements are the same as the Toga requirements, and it obviously requires Toga itself. Platform specifics can be seen here: [Toga Platform Requirements](https://toga.beeware.org/en/latest/reference/platforms/)

## Installation
In your Toga project's pyproject.toml, add:
```toml
requires = [
    "toga-tml",
]
``` 
In any python files in that project you want to use toga in, add the following code:
```python
import toga_tml
# ... other imports

class Example(toga.App):
    def startup(self):
        # ... other toga code
        self.main_window = toga.MainWindow(title=self.formal_name)
        # This can be changed depending on where your .xml or .tml file is
        tml_path = pathlib.Path(__file__).parent / "YOUR_XML_OR_TML_FILE_HERE" 
        self.main_window.content = toga_tml.load(tml_path, self=self)
        self.main_window.show()
    # ... other functions
```
Then run `briefcase dev -r` to run the project and rebuild dependencies.

## Usage
The syntax for TML is similar to HTML, except it uses Toga attributes and tag names. An example can be seen here:
```xml
<Body>
    <Label "Hello world" name="hi_label" style=Pack(color="#ff0000")/>
    <Box name="input_container"> 
        <TextInput name="name_input" flex=1/>
        <Button "Click me!" name="button" on_press=self.say_hello margin=5/>
    </Box>
</Body>
```
- All TML user interface code should be inside the `<Body></Body>` tags. 
- If you want to be able to refer to a TML element in a python file, a `name=""` must be added, and then you can refer to it with `self.name`. 
- All TML tags are self closing, except for `<Body></Body>` and `<Box></Box>`. This means that when using a label or a button, text that will be displayed on it must go in quotes after the tag opening, called the "argument" e.g. `<Label "Hello">`. 
- Any Toga attributes you wish to use in a tag can go after the argument, or if you don't have an argument, after the tag opening. The syntax for attributes will be the same as Toga syntax, except no commas separating attributes e.g. `<Label "Hi" name="label1" margin=5/>`.