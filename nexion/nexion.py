from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
source = open("/storage/emulated/0/nexion/examples/hello.nxn").read()
#print(source)
lexer = Lexer(source)
try:
    tokens = lexer.scan_tokens()
    statements = Parser(tokens).parse()
    Interpreter(statements).run()
    
except Exception as e:
    print(e)

#print(statements)
