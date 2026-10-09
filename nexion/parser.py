from AST.statements import LetStatement, AssignStatement, SayStatement, IfStatement, Block, WhileStatement, ExitStatement, NextStatement, Function, FunCall, ReturnStatement
from AST.program import Program
from AST.expressions import NumberLiteral, StringLiteral, Identifier, BinaryExpression, BooleanLiteral, UnaryExpression, NoneLiteral, ListLiteral, IndexExpression, IndexAssignment, DictLiteral, SliceExpression
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
            "MINUS",
            "LEFT_BRACKET",
            "LEFT_BRACE"
        ]
        self.valid_dict_keys = [
            "NUMBER",
            "STRING",
            "TRUE",
            "FALSE"
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
        expr = None
        if self.expect("NUMBER"):
            value = self.current().value
            self.advance()
            expr = NumberLiteral(value)
        elif self.expect("NOT"):
            self.advance()
            operand = self.parse_primary()
            expr = UnaryExpression("not", operand)
        elif self.expect("MINUS"):
            self.advance()
            operand = self.parse_primary()
            expr = UnaryExpression("minus", operand)
        elif self.expect("STRING"):
            value = self.current().value
            self.advance()
            expr = StringLiteral(value)
        elif self.expect("IDENTIFIER"):
            ident = Identifier(self.current().value)
            expr = ident
            self.advance()
            if self.expect("LEFT_PAREN"):
                expr = self.parse_funcall(ident)
        elif self.expect("TRUE", "FALSE"):
            value = self.current().type == "TRUE"
            self.advance()
            expr = BooleanLiteral(value)
        elif self.expect("LEFT_PAREN"):
            expr = self.parse_paren()
        elif self.expect("NONE"):
            self.advance()
            expr = NoneLiteral()
        elif self.expect("LEFT_BRACKET"):
            expr = self.parse_list()
        elif self.expect("LEFT_BRACE"):
            self.advance() #consune { initially
            expr = self.parse_dict()
        else:
            raise Exception(f"Syntax Error: Expected expression, found {self.current().value}")
        return self.parse_postfix(expr)
        
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
            
            statements.append(self.parse_statement())
        if self.is_eof():
            raise Exception("Unclosed '{'")
        self.advance() #consuming } at the end
        return Block(statements)
        
    def parse_binaryexpr(self, left, op, right):
       return BinaryExpression(left, op, right)
    def parse_expression(self, *end_tokens, min_prec=0):
        if not self.is_eof() and self.expect(*self.valid_expr_start):
            currToken = self.parse_primary()
            
            while not self.is_eof() and self.expect(*BINARY_OPERATORS):
                op = self.current().value
                if PRECEDENCE[op] <= min_prec:
                    return currToken
                self.advance()
                right = self.parse_expression(*end_tokens, min_prec=PRECEDENCE[op])
                currToken = self.parse_binaryexpr(currToken, op, right)
            if not self.is_eof():
                if self.expect(*end_tokens):
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
    def parse_assignment(self, var_name):
        expr=None
        if not self.is_eof() and self.expect("ASSIGN"):
             self.advance()
        else:
             raise Exception("Syntax Error: Expected '='.")
        if self.expect(*self.valid_expr_start):
             expr = self.parse_expression("SEMI_COLON")
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
     
    def parse_funcall(self, fun_name):
        arguments=[]
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
                    return FunCall(fun_name, arguments)
                else:
                    raise Exception(f"Syntax Error: Expected ',' or ')', Found: {self.current().type}")
                
        else:
            raise Exception(f"Syntax Error: Expected '(', Found {self.current().value}")
            
    def parse_list(self):
        self.advance()
        elements = []
        if not self.is_eof() and self.expect("RIGHT_BRACKET"):
            self.advance()
            return ListLiteral()
        elif not self.is_eof() and self.expect(*self.valid_expr_start):
            elements.append(self.parse_expression("COMMA", "RIGHT_BRACKET"))
            while not self.is_eof() and (self.expect("COMMA")):
                self.advance()
                elements.append(self.parse_expression("COMMA", "RIGHT_BRACKET"))
            if not self.is_eof() and self.expect("RIGHT_BRACKET"):
                self.advance()
                return ListLiteral(elements)
        else:
            raise Exception("Syntax Error: Expected an Expression")
            
    def parse_index(self, target):
        while not self.is_eof() and self.expect("LEFT_BRACKET"):
            self.advance()
            if self.expect("COLON"): # if [:] or [:end]
                self.advance()
                if not self.is_eof() and self.expect("RIGHT_BRACKET"): #if [:]
                    target = SliceExpression(target)
                elif not self.is_eof() and self.expect(*self.valid_expr_start):
                    target = SliceExpression(target, None, self.parse_expression("RIGHT_BRACKET"))
            elif self.expect(*self.valid_expr_start): 
                #if [start:end] or [start:]
                index = self.parse_expression("COLON", "RIGHT_BRACKET")
                if not self.is_eof() and self.expect("COLON"):
                    #if [start:]
                    self.advance()
                    if not self.is_eof() and self.expect(*self.valid_expr_start): #if [start:end]
                        end = self.parse_expression("RIGHT_BRACKET")
                        target = SliceExpression(target, index, end)
                    elif not self.is_eof() and self.expect("RIGHT_BRACKET"): #if [start:]
                        target = SliceExpression(target, index)
                else:
                    target = IndexExpression(target, index)
            if self.is_eof() or not self.expect("RIGHT_BRACKET"):
                raise Exception("Syntax Error: Missing ']'")
            self.advance()
        return target
                
    def parse_postfix(self, expr):
        if not self.is_eof() and self.expect("LEFT_BRACKET"):
            return self.parse_index(expr)
        return expr
    def parse_index_assignment(self, target):
        self.advance()
        if (not self.is_eof() and self.expect(*self.valid_expr_start)):
            value = self.parse_primary()
            return IndexAssignment(target, value) 
        else:
            raise Exception("Syntax error: Expected an Expression.")
    def parse_dict(self, entries=None):
        if entries is None:
            entries = []
        if self.expect("RIGHT_BRACE") and entries in [None, []]:
            self.advance()
            return DictLiteral()
        if not self.is_eof() and not self.expect(*self.valid_dict_keys):
            raise Exception("Syntax Error: Dictionary keys must be a number, string, or boolean.")
        key = self.parse_primary()
        
        if not self.is_eof() and not self.expect("COLON"):
            raise Exception("Syntax Error: Expected ':' after dictionary key.")
        self.advance()
        
        if not self.is_eof() and not self.expect(*self.valid_expr_start):
            raise Exception("Syntax Error: Expected a value after ':'.")
        value = self.parse_expression("COMMA", "RIGHT_BRACE")
        entries.append([key, value])
        if not self.is_eof() and self.expect("COMMA"):
            self.advance()
            return self.parse_dict(entries)
        if not self.is_eof() and self.expect("RIGHT_BRACE"):
            self.advance()
            return DictLiteral(entries)
        raise Exception("Syntax Error: Missing '}'")
    def parse_statement(self):
        if self.expect("LET"):
            return self.parse_let()
        elif self.expect("IDENTIFIER"):
            ident = Identifier(self.current().value)
            self.advance()
            if self.is_eof():
                raise Exception("Syntax Error: Missing ';'")
            if self.expect("ASSIGN"):
                return self.parse_assignment(ident)
            elif self.expect("LEFT_PAREN"):
                ast = self.parse_funcall(ident)
                self.advance()
                return ast
            elif self.expect("LEFT_BRACKET"):
                ast = self.parse_index(ident)
                if not self.is_eof() and self.expect("ASSIGN"):
                    ast = self.parse_index_assignment(ast)
                    if not self.is_eof() and not self.expect("SEMI_COLON"):
                        raise Exception("Syntax Error: Missing ';'")
                    self.advance()
                    return ast
                if not self.is_eof() and self.expect("SEMI_COLON"):
                    self.advance()
                    return ast
                raise Exception("Syntax Error: Missing ';'")
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
        elif self.expect("LEFT_BRACKET"):
            ast = self.parse_list()
            if not self.is_eof() and self.expect("SEMI_COLON"):
                self.advance()
                return ast
            raise Exception("Syntax Error: Expected ';'")
        else:
            raise Exception(f"Syntax Error: Unknown token: '{self.current().value}', at {self.position}")
    def parse(self):
        while not self.is_eof():
            self.statements.append(self.parse_statement())
        #print(self.statements)
        return Program(self.statements)
        