import lexer
import parser
import generator

def load(file):
    with open(file, "r", encoding="utf-8") as file:
        tml = file.read()
    tokens = lexer.tokenize(tml)
    parsed = parser.parse(tokens)
    output = generator.generate(parsed)
    print("Loaded")
    return output


print(load("src/tml/example.xml"))