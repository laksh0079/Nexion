from lexer import Lexer
from parser import Parser
source = open("/storage/emulated/0/Prism/examples/hello.px").read()
#print(source)
lexer = Lexer(source)
tokens = lexer.scan_tokens()
parser = Parser(tokens)
print(tokens)
parser.parse()