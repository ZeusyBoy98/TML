import sys
from . import generator, lexer, parser


def load(file, self=None):
    with open(file, "r", encoding="utf-8") as f:
        tml_source = f.read()
    tokens = lexer.tokenize(tml_source)
    parsed = parser.parse(tokens)
    output = generator.generate(parsed)
    namespace = {"self": self}
    exec("import toga\n" + output, namespace)
    if "body" not in namespace:
        raise RuntimeError("M001 - The TML code does not contain a 'Body' widget.")
    return namespace["body"]

def main():
    if len(sys.argv) < 2:
        print("Usage: tml <file.xml>")
        sys.exit(1)
    output = load(sys.argv[1])
    print(output)

if __name__ == "__main__":
    main()
