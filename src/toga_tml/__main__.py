import sys
from . import lexer
from . import parser
from . import generator

def load(file, self):
    with open(file, "r", encoding="utf-8") as f:
        tml_source = f.read()
    tokens = lexer.tokenize(tml_source)
    parsed = parser.parse(tokens)
    output = generator.generate(parsed)
    namespace = {"self": self}
    exec("import toga\nfrom toga.style import Pack\n" + output, namespace)
    if "main_box" not in namespace:
        raise RuntimeError("Generated TML code did not produce a 'main_box' widget")
    return namespace["main_box"]

def main():
    if len(sys.argv) < 2:
        print("Usage: tml <file.xml>")
        sys.exit(1)
    output = load(sys.argv[1])
    print(output)

if __name__ == "__main__":
    main()