from operators import OPERATORS, OPERATOR_STARTS

class Lexer:
    keywords = {
        "set": "SET",
        "to": "TO",
        "say": "SAY",
        "true": "TRUE",
        "false": "FALSE",
        "not": "NOT",
        "and": "AND",
        "or": "OR"
   }
    
    symbols = {
        ";": "SEMI_COLON",
        "(": "LEFT_PAREN",
        ")": "RIGHT_PAREN"
    }
    
    def __init__(self, source):
        self.source = source
        self.current=0
        self.tokens=[]
        
    def scan_identifier(self):
        word=""
        while self.current < len(self.source) and (self.source[self.current].isalpha() or self.source[self.current].isdigit()):
            word+=self.source[self.current]
            self.current+=1
        if word in self.keywords.keys():
            self.tokens.append((self.keywords[word], word))
        else:
            self.tokens.append(("IDENTIFIER", word))
    
    def scan_number(self):
        digits=""
        while self.current < len(self.source) and (self.source[self.current].isdigit()):
            digits+=self.source[self.current]
            self.current+=1
        if self.current<len(self.source) and self.source[self.current].isalpha():
            raise Exception("Lexical Error: Identifier cannor start with a digit.")
        else:
            self.tokens.append(("NUMBER", int(digits)))
                
                
    def scan_symbols(self):
        if self.source[self.current] in self.symbols:
            self.tokens.append((self.symbols[self.source[self.current]], self.source[self.current]))
        else:
            raise Exception(f"Lexical Error: UNKNOWN SYMBOL: {self.source[self.current]}.")
        self.current+=1
        
    def scan_string(self):
        text=""
        quote_closed=False
        self.current+=1
        while self.current < len(self.source):
            if self.source[self.current] == '"':
                self.current+=1
                quote_closed=True
                break
            text+=self.source[self.current]
            self.current+=1
        if self.current > len(self.source) or (not quote_closed):
            raise Exception("Lexical Error: Unterminated string.")
        self.tokens.append(("STRING", text))
        #print(text, self.tokens)
    def scan_operator(self):
        operator = self.source[self.current]
        if self.current + 1 < len(self.source):
            next_operator = self.source[self.current+1]
            if operator + next_operator in OPERATORS:
                operator += next_operator
                self.current+=1
        self.tokens.append((OPERATORS[operator], operator))
        self.current += 1

    def scan_tokens(self):
        while self.current < len(self.source):
            if self.current < len(self.source) and self.source[self.current].isspace():
                self.current+=1
            elif self.current < len(self.source) and self.source[self.current].isalpha():
                self.scan_identifier()
            elif self.current < len(self.source) and self.source[self.current].isdigit():
                self.scan_number()
            elif self.current < len(self.source) and self.source[self.current] == '"':
                self.scan_string()
            elif self.current < len(self.source) and self.source[self.current] in OPERATOR_STARTS:
                self.scan_operator()
            elif self.current < len(self.source) and (not self.source[self.current].isalnum()):
                self.scan_symbols()
            else:
                raise Exception("Lexical Error: Unknown Error")
        print(self.tokens)
        return self.tokens