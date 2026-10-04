from AST.statements import LetStatement, AssignStatement, SayStatement, IfStatement, Block, WhileStatement, ExitStatement, NextStatement, Function, FunCall, ReturnStatement
from AST.program import Program
from AST.expressions import NumberLiteral, StringLiteral, Identifier, BinaryExpression, BooleanLiteral, UnaryExpression, NoneLiteral
from operators import PRECEDENCE,BINARY_OPERATORS
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.statements=[]
        self.valid_expr_start = [
            "LEFT_PAREN",
            "IDENTIFIER",
            "NUMBER",
            "STRING",
            "TRUE",
            "FALSE",
            "NOT",
            "NONE",
            "MINUS"
        ]
    
    def is_eof(self):
        return self.position >= len(self.tokens)
        
    def advance(self):
        self.position += 1
        
    def peek(self):
        if self.position + 1 >= len(self.tokens):
            return None
        return self.tokens[self.position + 1]
    def current(self):
        return self.tokens[self.position]
        
    def expect(self, *expected):
        return self.current().type in expected
    def parse_primary(self):
        if self.expect("NUMBER"):
            value = self.current().value
            self.advance()
            return NumberLiteral(value)
        elif self.expect("NOT"):
            self.advance()
            operand = self.parse_primary()
            return UnaryExpression("not", operand)
        elif self.expect("MINUS"):
            self.advance()
            operand = self.parse_primary()
            return UnaryExpression("minus", operand)
        elif self.expect("STRING"):
            value = self.current().value
            self.advance()
            return StringLiteral(value)
        elif self.expect("IDENTIFIER"):
            if self.peek().type == "LEFT_PAREN":
                return self.parse_funcall()
            value = self.current().value
            self.advance()
            return Identifier(value)
        elif self.expect("TRUE", "FALSE"):
            value = self.current().type == "TRUE"
            self.advance()
            return BooleanLiteral(value)
        elif self.expect("LEFT_PAREN"):
            return self.parse_paren()
        elif self.expect("NONE"):
            self.advance()
            return NoneLiteral()
        else:
            raise Exception(f"Syntax Error: Expected expression, found {self.current().value}")
            
    def parse_paren(self):
        self.advance()
        expr = self.parse_expression("RIGHT_PAREN")
        if self.is_eof():
            raise Exception("Unclosed parentheses")
        if not self.expect("RIGHT_PAREN"):
            raise Exception("Expected ')'")
        self.advance()
        return expr
        
    def parse_block(self):
        self.advance() #consuming { at the start
        statements = []
        while (not self.is_eof()) and (not self.expect("RIGHT_BRACE")):
            #parse statements and append to the list
            #print(self.tokens[self.current])
            statements.append(self.parse_statement())
        if self.is_eof():
            raise Exception("Unclosed '{'")
        self.advance() #consuming } at the end
        return Block(statements)
        
    def parse_binaryexpr(self, left, op, right, end_token):
       return BinaryExpression(left, op, right)
    def parse_expression(self, end_token, min_prec=0):
        if not self.is_eof() and self.expect(*self.valid_expr_start):
            currToken = self.parse_primary()
            
            while not self.is_eof() and self.expect(*BINARY_OPERATORS):
                op = self.current().value
                if PRECEDENCE[op] <= min_prec:
                    return currToken
                self.advance()
                right = self.parse_expression(end_token, PRECEDENCE[op])
                currToken = self.parse_binaryexpr(currToken, op, right, end_token)
            if not self.is_eof():
                if self.expect(end_token):
                    return currToken
                return currToken
            else:
                raise Exception("Expected an expression or end token")
        
        else:
            raise Exception("Expected Expression")
        
    def parse_let(self):
        var_name=None
        expr=None
        self.advance()
        if self.expect("IDENTIFIER"):
             var_name = self.current().value
             self.advance()
        else:
             raise Exception("Syntax Error: Expected an indentifier.")
        if not self.is_eof() and self.expect("ASSIGN"):
             self.advance()
        else:
             raise Exception("Syntax Error: Expected '='.")
        if self.expect(*self.valid_expr_start):
             expr = self.parse_expression("SEMI_COLON")
             #print(expr)
             # self.current+=1
        else:
             raise Exception("Syntax Error: Expected a value.")
        if self.is_eof():
             raise Exception("Syntax Error: missing ';'.")
        else:
             if self.expect("SEMI_COLON"):
                 self.advance()
             else:
                 raise Exception("Syntax Error: Expected';'.")
        return LetStatement(Identifier(var_name), expr)
    def parse_assignment(self):
        var_name= self.current().value
        expr=None
        self.advance()
        if not self.is_eof() and self.expect("ASSIGN"):
             self.advance()
        else:
             raise Exception("Syntax Error: Expected '='.")
        if self.expect(*self.valid_expr_start):
             expr = self.parse_expression("SEMI_COLON")
             #print(expr)
        else:
             raise Exception("Syntax Error: Expected a value.")
        if self.is_eof():
             raise Exception("Syntax Error: missing ';'.")
        else:
             if self.expect("SEMI_COLON"):
                 self.advance()
             else:
                 raise Exception("Syntax Error: Expected';'.")
        return AssignStatement(Identifier(var_name), expr)
    def parse_say(self):
        arg=None
        self.advance()
        if self.is_eof():
            raise Exception("Syntax Error: Expected '('.")
        elif self.expect("LEFT_PAREN"):
            self.advance()
        else:
            raise Exception("Syntax Error: Expected '('.")
        if self.is_eof():
            raise Exception("Syntax Error: Expected an indentifier.")
        elif self.expect(*self.valid_expr_start):
            arg = self.parse_expression("RIGHT_PAREN")
            #print(arg)
        else:
            raise Exception("Syntax Error: Expected an indentifier.")
        if self.is_eof():
            raise Exception("Syntax Error: Expected  ')'.")
        elif self.expect("RIGHT_PAREN"):
            self.advance()
        else:
            raise Exception("Syntax Error: Expected  ')'.")
        if self.is_eof():
            raise Exception("Syntax error: missing ';'.")
        else:
            if self.expect("SEMI_COLON"):
                self.advance()
            else:
                raise Exception(f"Syntax error: Expected: ';', Found: '{self.current().type}'.")
        return SayStatement(arg)
    # refactor left from here
    def parse_if(self):
        condition = None
        statements = None
        else_branch = None
        self.advance()
        if not self.is_eof() and self.expect(*self.valid_expr_start):
            condition = self.parse_expression("LEFT_BRACE")
            #print(condition)
        else:
            raise Exception("Syntax Erorr: Expected an Expression")
        if self.expect("LEFT_BRACE"):
            statements = self.parse_block()
            if not self.is_eof() and self.expect("ELSE"):
                self.advance()
                if not self.is_eof() and self.expect("IF"):
                    else_branch = self.parse_if()
                else:
                    if not self.is_eof() and  self.expect("LEFT_BRACE"):
                        else_branch = self.parse_block()
                    else:
                        raise Exception(f"Syntax Error: Expected '{{' Found {self.current().value}")
        else:
            raise Exception(f"Syntax Error: Expected '{{' Found {self.current().value}")
        #print(IfStatement(condition, statements))
        return IfStatement(condition, statements, else_branch)
    def parse_while(self):
        condition = None
        statements = None
        self.advance()
        if not self.is_eof() and self.expect(*self.valid_expr_start):
            condition = self.parse_expression("LEFT_BRACE")
        else:
            raise Exception("Syntax Erorr: Expected an Expression")
        if not self.is_eof() and self.expect("LEFT_BRACE"):
            statements = self.parse_block()
        else:
            raise Exception(f"Syntax Error: Expected '{{' Found {self.current().value}")
        return WhileStatement(condition, statements)
        
    def parse_return(self):
        self.advance()
        if not self.is_eof() and self.expect("SEMI_COLON"):
            self.advance()
            return ReturnStatement()
        elif self.expect(*self.valid_expr_start):
            return_value = self.parse_expression("SEMI_COLON")
            self.advance()
            print(self.current())
            return ReturnStatement(return_value)
        else:
            raise Exception("Syntax Error: Missing Semicolon")

    def parse_control(self):
        control = None
        if self.expect("EXIT"):
            control = ExitStatement()
            self.advance()
            if not self.is_eof() and self.expect("SEMI_COLON"):
                self.advance()#consume ;
            else:
                raise Exception("Syntax Error: Missing Semicolon")
        elif self.expect("NEXT"):
            control = NextStatement()
            self.advance()
            if not self.is_eof() and self.expect("SEMI_COLON"):
                self.advance()
            else:
                raise Exception("Syntax Error: Missing Semicolon")
        return control
    def parse_function(self):
        parameters = []
        block = None
        self.advance() #consume fun
        if self.is_eof():
            raise Exception("Syntax Error: Expected '('")
        elif not self.expect("IDENTIFIER"):
            raise Exception(f"Syntax Erorr: Expected Function Name, Found {self.current().value}")
        fun_name = self.current().value
        self.advance()
        if not self.is_eof() and self.expect("LEFT_PAREN"):
            self.advance()
            if self.is_eof():
                raise Exception("Syntax Error: Missing ')'")
            if self.expect("RIGHT_PAREN"):
                self.advance()
                block = self.parse_block()
                return Function(fun_name, None, block)
            elif not self.is_eof() and self.expect("IDENTIFIER"):
                parameters.append(self.parse_primary())
                while not self.is_eof() and self.expect("COMMA"):
                    self.advance()
                    if not self.is_eof() and self.expect("RIGHT_PAREN"):
                        raise Exception("Syntax Error: Expected Parameter After Comma")
                    if not self.is_eof() and not self.expect("IDENTIFIER"):
                        raise Exception(f"Syntax Error: Expected Parameter, Found: {self.current().type}")
                    parameters.append(self.parse_primary())
                if not self.is_eof() and self.expect("RIGHT_PAREN"):
                    self.advance()
                    block = self.parse_block()
                    return Function(fun_name, parameters, block)
                else:
                    raise Exception(f"Syntax Error: Expected ',' or ')', Found: {self.current().type}")
            else:
                raise Exception(f"Syntax Error: Expected a Parameter, Found: {self.current().type}")
                
        else:
            raise Exception(f"Syntax Error: Expected '(', Found {self.current().value}")
     
    def parse_funcall(self):
        fun_name = self.current().value
        arguments=[]
        self.advance()
        if not self.is_eof() and self.expect("LEFT_PAREN"):
            self.advance()
            if self.is_eof():
                raise Exception("Syntax Error: Expected ')'")
            if self.current().type == "RIGHT_PAREN":
                self.advance()
                return FunCall(fun_name)
            elif self.expect(*self.valid_expr_start):
                arguments.append(self.parse_expression("COMMA"))
                while not self.is_eof() and self.expect("COMMA"):
                    self.advance()
                    if not self.is_eof() and self.expect("RIGHT_PAREN"):
                        raise Exception("Syntax Error: Expected Argument After Comma")
                    arguments.append(self.parse_expression("COMMA"))
                if not self.is_eof() and self.expect("RIGHT_PAREN"):
                    self.advance()
                    print("FUNCALL:", fun_name, arguments)
                    return FunCall(fun_name, arguments)
                else:
                    raise Exception(f"Syntax Error: Expected ',' or ')', Found: {self.current().type}")
                
        else:
            raise Exception(f"Syntax Error: Expected '(', Found {self.current().value}")
    def parse_statement(self):
        if self.expect("LET"):
            return self.parse_let()
        elif self.expect("IDENTIFIER") and self.peek().type == "ASSIGN":
            return self.parse_assignment()
        elif self.expect("IDENTIFIER") and self.peek().type == "LEFT_PAREN":
            ast = self.parse_funcall()
            self.advance()
            return ast
        elif self.expect("SAY"):
            return self.parse_say()
        elif self.expect("IF"):
            return self.parse_if()
        elif self.expect("LEFT_BRACE"):
            return self.parse_block()
        elif self.expect("WHILE"):
            return self.parse_while()
        elif self.expect(*["EXIT", "NEXT"]):
            return self.parse_control()
        elif self.expect("FUN"):
            return self.parse_function()
        elif self.expect("RETURN"):
            return self.parse_return()
        else:
            raise Exception(f"Syntax Error: Unknown token: '{self.current().value}', at {self.position}")
    def parse(self):
        while not self.is_eof():
            self.statements.append(self.parse_statement())
        #print(self.statements)
        return Program(self.statements)
          