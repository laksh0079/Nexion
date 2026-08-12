from AST.statements import SetStatement, SayStatement
from AST.program import Program
from AST.expressions import NumberLiteral, StringLiteral, Identifier, BinaryExpression, BooleanLiteral, UnaryExpression
from operators import PRECEDENCE,BINARY_OPERATORS
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.statements=[]
        self.valid_expr_start = [
            "LEFT_PAREN",
            "IDENTIFIER",
            "NUMBER",
            "STRING",
            "TRUE",
            "FALSE",
            "NOT"
        ]
    def parse_primary(self):
        if self.tokens[self.current][0] == "NUMBER":
            value = self.tokens[self.current][1]
            self.current+=1
            return NumberLiteral(value)
        elif self.tokens[self.current][0] == "NOT":
            self.current +=1
            operand = self.parse_primary()
            return UnaryExpression("not", operand)
        elif self.tokens[self.current][0] == "STRING":
            value = self.tokens[self.current][1]
            self.current+=1
            return StringLiteral(value)
        elif self.tokens[self.current][0] == "IDENTIFIER":
            value = self.tokens[self.current][1]
            self.current+=1
            return Identifier(value)
        elif self.tokens[self.current][0] in ["TRUE", "FALSE"]:
            value = self.tokens[self.current][1].lower() == "true"
            self.current +=1
            return BooleanLiteral(value)
        elif self.tokens[self.current][0] == "LEFT_PAREN":
            return self.parse_paren()
        else:
            raise Exception(f"Syntax Error: Expected expression, found {self.tokens[self.current][0]}")
    def parse_paren(self):
        self.current +=1
        expr = self.parse_expression("RIGHT_PAREN")
        if self.current >= len(self.tokens):
            raise Exception("Unclosed parentheses")
        if self.tokens[self.current][1] != ')':
            raise Exception("Expected ')'")
        self.current+=1
        return expr
    def parse_binaryexpr(self, left, op, right, end_token):
       return BinaryExpression(left, op, right)
    def parse_expression(self, end_token, min_prec=0):
        if self.current < len(self.tokens) and  self.tokens[self.current][0] in self.valid_expr_start:
            currToken = self.parse_primary()
            
            while self.current < len(self.tokens) and self.tokens[self.current][0] in BINARY_OPERATORS:
                op = self.tokens[self.current][1]
                if PRECEDENCE[op] <= min_prec:
                    return currToken
                self.current += 1
                right = self.parse_expression(end_token, PRECEDENCE[op])
                currToken = self.parse_binaryexpr(currToken, op, right, end_token)
            if self.current < len(self.tokens):
                if self.tokens[self.current][0] == end_token:
                    return currToken
                else:
                    raise Exception("Expected an expression or end token")
            else:
                raise Exception("Expected an expression or end token")
        
        else:
            raise Exception("Expected Expression")
        
    def parse_set(self):
        var_name=None
        expr=None
        self.current+=1
        if self.tokens[self.current][0] == "IDENTIFIER":
             var_name = self.tokens[self.current][1]
             self.current+=1
        else:
             raise Exception("Syntax Error: Expected an indentifier.")
        if self.current < len(self.tokens) and self.tokens[self.current][0] == "TO":
             self.current+=1
             
        else:
             raise Exception("Syntax Error: Expected 'to'.")
        if self.tokens[self.current][0] in self.valid_expr_start:
             expr = self.parse_expression("SEMI_COLON")
             print(expr)
             # self.current+=1
        else:
             raise Exception("Syntax Error: Expected a value.")
        if self.current >= len(self.tokens):
             raise Exception("Syntax Error: missing ';'.")
        else:
             if self.tokens[self.current][0] == "SEMI_COLON":
                 self.current+=1
             else:
                 raise Exception("Syntax Error: Expected';'.")
        return SetStatement(Identifier(var_name), expr)
    def parse_say(self):
        arg=None
        self.current+=1
        if self.current >= len(self.tokens):
            raise Exception("Syntax Error: Expected '('.")
        elif self.tokens[self.current][0] == "LEFT_PAREN":
            self.current+=1
        else:
            raise Exception("Syntax Error: Expected '('.")
        if self.current >= len(self.tokens):
            raise Exception("Syntax Error: Expected an indentifier.")
        elif self.tokens[self.current][0] in ["IDENTIFIER", "NUMBER", "STRING", "LEFT_PAREN"]:
            arg = self.parse_expression("RIGHT_PAREN")
            #print(arg)
        else:
            raise Exception("Syntax Error: Expected an indentifier.")
        if self.current >= len(self.tokens):
            raise Exception("Syntax Error: Expected  ')'.")
        elif self.tokens[self.current][0] == "RIGHT_PAREN":
            self.current+=1
        else:
            raise Exception("Syntax Error: Expected  ')'.")
        if self.current >= len(self.tokens):
            raise Exception("Syntax error: missing ';'.")
        else:
            if self.tokens[self.current][0] == "SEMI_COLON":
                self.current+=1
            else:
                raise Exception(f"Syntax error: Expected: ';', Found: '{self.tokens[self.current][1]}'.")
        return SayStatement(arg)
    
    def parse(self):
        while self.current < len(self.tokens):
            if self.tokens[self.current][0] == "SET":
                self.statements.append(self.parse_set())
            elif self.tokens[self.current][0] == "SAY":
                self.statements.append(self.parse_say())
            else:
                 raise Exception(f"Syntax Error: Unknown token: '{self.tokens[self.current][1]}'")
        return Program(self.statements)
          