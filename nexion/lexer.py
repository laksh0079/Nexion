from operators import OPERATORS, OPERATOR_STARTS
from dataclasses import dataclass
@dataclass
class Token:
    type: str
    value: object
class Lexer:
    keywords = {
        "let": "LET",
        "say": "SAY",
        "true": "TRUE",
        "false": "FALSE",
        "not": "NOT",
        "and": "AND",
        "or": "OR",
        "if": "IF",
        "else": "ELSE",
        "while": "WHILE",
        "exit": "EXIT",
        "next": "NEXT",
        "fun": "FUN",
        "none": "NONE",
        "return": "RETURN"
   }
    
    symbols = {
        ";": "SEMI_COLON",
        "(": "LEFT_PAREN",
        ")": "RIGHT_PAREN",
        "{": "LEFT_BRACE",
        "}": "RIGHT_BRACE",
        ",": "COMMA",
        "_": "UNDERSCORE",
        "[": "LEFT_BRACKET",
        "]": "RIGHT_BRACKET"
    }
    
    def __init__(self, source):
        self.source = source
        self.position=0
        self.tokens=[]
    def current(self):
        return self.source[self.position]
    def advance(self):
        self.position += 1
    def peek(self):
        if self.position + 1 >= len(self.source):
            return None
        return self.source[self.position + 1]
    def is_eof(self):
        return self.position >= len(self.source)
    def scan_identifier(self):
        word=""
        while not self.is_eof() and (self.current().isalpha() or self.current().isdigit() or self.current() == "_"):
            word+=self.current()
            self.advance()
        if word in self.keywords.keys():
            self.tokens.append(Token(self.keywords[word], word))
        else:
            self.tokens.append(Token("IDENTIFIER", word))
    
    def scan_number(self):
        digits=""
        while not self.is_eof() and (self.current().isdigit()):
            digits+=self.current()
            self.advance()
        if not self.is_eof() and self.current().isalpha():
            raise Exception("Lexical Error: Identifier cannor start with a digit.")
        else:
            self.tokens.append(Token("NUMBER", int(digits)))
                
                
    def scan_symbols(self):
        if self.current() in self.symbols:
            self.tokens.append(Token(self.symbols[self.current()], self.current()))
        else:
            raise Exception(f"Lexical Error: UNKNOWN SYMBOL: {self.current()}.")
        self.advance()
        
    def scan_string(self):
        text=""
        quote_closed=False
        self.advance()
        while not self.is_eof():
            if self.current() == '"':
                self.advance()
                quote_closed=True
                break
            text+=self.current()
            self.advance()
        if self.is_eof() or (not quote_closed):
            raise Exception("Lexical Error: Unterminated string.")
        self.tokens.append(Token("STRING", text))
        #print(text, self.tokens)
    def scan_operator(self):
        operator = self.current()
        if self.position + 1 < len(self.source):
            next_operator = self.source[self.position+1]
            if operator + next_operator in OPERATORS:
                operator += next_operator
                self.advance()
        self.tokens.append(Token(OPERATORS[operator], operator))
        self.advance()

    def scan_tokens(self):
        while not self.is_eof():
            if self.current() == "/" and self.peek() == "/":
                while not self.is_eof() and not self.current() == "\n":
                    self.advance()
            elif self.current().isspace():
                self.advance()
            elif self.current().isalpha() or self.current() == "_":
                self.scan_identifier()
            elif self.current().isdigit():
                self.scan_number()
            elif self.current() == '"':
                self.scan_string()
            elif self.current() in OPERATOR_STARTS:
                self.scan_operator()
            elif (not self.current().isalnum()):
                self.scan_symbols()
            else:
                raise Exception("Lexical Error: Unknown Error")
        #print(self.tokens)
        return self.tokens