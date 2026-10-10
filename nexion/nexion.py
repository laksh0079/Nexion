from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "/storage/emulated/0/nexion/examples/hello.nxn"

source = open(filename).read()
print(source)
lexer = Lexer(source)
try:
    tokens = lexer.scan_tokens()
    statements = Parser(tokens).parse()
    Interpreter(statements).run()
    
except Exception as e:
    print(e)

#print(statements)
