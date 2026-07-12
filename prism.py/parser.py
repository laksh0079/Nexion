class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        
        
    def parse(self):
        while self.current < len(self.tokens):
            if self.tokens[self.current][0] == "SET":
                self.current+=1
                if self.tokens[self.current][0] == "IDENTIFIER":
                    self.current+=1
                else:
                     print("Syntax error: Expected an indentifier")
                     break
                if self.tokens[self.current][0] == "TO":
                     self.current+=1
                else:
                    print("Syntax error: Expected assignment operator 'to' ")
                 
                    break
                if self.tokens[self.current][0] == "NUMBER" or self.tokens[self.current][0] == "IDENTIFIER":
                     self.current+=1
                else:
                     print("Expected a value!")
                     break
                if self.current == len(self.tokens):
                    print("Syntax error: missing a semicolon (;)")
                    break
                else:
                    if self.tokens[self.current][0] == "SEMI_COLON":
                         self.current+=1
                    else:
                        print("Syntax error: missing a semicolon (;)")
                        break
            elif self.tokens[self.current][0] == "SAY":
                self.current+=1
                if self.current == len(self.tokens):
                    print("Expected a '('")
                    break
                elif self.tokens[self.current][0] == "LEFT_PAREN":
                    self.current+=1
                else:
                    print("Expected a '('")
                    break
                if self.current == len(self.tokens):
                    print("Expected an indentifier")
                    break
                elif self.tokens[self.current][0] == "IDENTIFIER" or self.tokens[self.current][0] == "NUMBER":
                    self.current+=1
                else:
                    print("Expected an indentifier")
                    break
                if self.current == len(self.tokens):
                    print("Expected a ')'")
                    break
                elif self.tokens[self.current][0] == "RIGHT_PAREN":
                    self.current+=1
                else:
                     print("Expected a ')'")
                if self.current == len(self.tokens):
                     print("Syntax error: missing a semicolon(;)")
                     break
                else:
                     if self.tokens[self.current][0] == "SEMI_COLON":
                         self.current+=1
                     else:
                         print("Syntax error: missing a semicolon (;)")
                         break
            else:
                 print("Syntax error!!")
                 break
            print("Parsed statement Successfully")
            