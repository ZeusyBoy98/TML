import lexer
import parser

tokens = lexer.tokenize("<test/><test2/><body/>")
print(parser.parse(tokens))