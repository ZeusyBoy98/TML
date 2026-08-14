import lexer
import parser
import generator

tokens = lexer.tokenize("<Label/><Gigma/><Body/>")
parsed = parser.parse(tokens)
print(generator.generate(parsed))