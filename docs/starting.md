# Getting Started

## Requirements
The TML requirements are the same as the Toga requirements, and it obviously requires Toga itself. Platform specifics can be seen here: [Toga Platform Requirements](https://toga.beeware.org/en/latest/reference/platforms/) <br>
It is recommended to use TML and Toga with BeeWare, as it allows for cross-platform python app development but simple.

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
Then run `briefcase dev -r` to run the project and rebuild dependencies (if you are using BeeWare).