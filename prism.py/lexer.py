class Lexer:
    keywords = {
        "set": "SET",
        "to": "TO",
        "say": "SAY"
    }
    
    symbols = {
        "=": "EQUALS",
        ";": "SEMI_COLON",
        "(": "LEFT_PAREN",
        ")": "RIGHT_PAREN"
    }
    def __init__(self, source):
        self.source = source
        self.current=0

    def scan_tokens(self):
        tokens=[]
        while self.current < len(self.source):
            if self.source[self.current].isalpha():
                word=""
                while self.current < len(self.source) and self.source[self.current].isalpha():
                    word+=self.source[self.current]
                    self.current+=1
                if word in self.keywords.keys():
                    tokens.append((self.keywords[word], word))
                else:
                    tokens.append(("IDENTIFIER", word))
            else:
                if self.source[self.current] == " ":
                    self.current+=1
                    continue
                elif self.source[self.current].isdigit():
                    digits=""
                    while self.current < len(self.source) and self.source[self.current].isdigit():
                        digits+=self.source[self.current]
                        self.current+=1
                    tokens.append(("NUMBER", int(digits)))
                elif self.source[self.current] == "\n":
                    self.current+=1
                    continue
                else:
                    if self.source[self.current] in self.symbols:
                        tokens.append((self.symbols[self.source[self.current]], self.source[self.current]))
                    else:
                        print(f"UNKNOWN SYMBOL: {self.source[self.current]}")
                    self.current+=1
        return tokens