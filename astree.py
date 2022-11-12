from tokens import Token

class Variable:
    STR = "STR"
    NUMBER = "NUMBER"
    BOOL = "BOOL"
    def __init__(self,name:str,value):
        if type(value) == int or type(value) == float:
            self.type = Variable.NUMBER
        elif type(value) == str:
            self.type = Variable.STR
        elif type(value) == bool:
            self.type = Variable.BOOL
        else:
            raise Exception("[!] variable type error.")

        self.name = name
        self.value = value

class Environment:
    def __init__(self):
        self.env = {}

    def get(self,name:str):
        if name in self.env:
            return self.env[name].value
        return None

    def put(self,name:str,var:Variable):
        self.env[name] = var

    def __setitem__(self,key:str,value):
        v = Variable(key,value)
        self.put(key,v)

    def __getitem__(self, key:str):
        return self.get(key)

class AST:
    PROGRAM = "PROGRAM"
    STATEMENTS = "STATEMENTS"
    STATEMENT = "STATEMENT"
    IFSTATEMENT = "IFSTATEMENT"
    WHILESTATEMENT = "WHILESTATEMENT"
    EXPR = "EXPR"
    EMPTY = "EMPTY"
    BLOCK = "BLOCK"
    FACTOR = "FACTOR"
    PRIMARY = "PRIMARY"
    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    PUNCT = "PUNCT"
    LEAF = "LEAF"
    OP = "OP"
    EOL = "EOL"

    def __init__(self,type:str,value:Token):
        self.children = []
        self.type = type
        self.value = value

    def add_child(self,ast):
        self.children.append(ast)

    def set_children(self,ast_list:list):
        self.children = ast_list

    @classmethod
    def debug(cls):
        del AST.PROGRAM
        del AST.STATEMENTS
        del AST.STATEMENT
        del AST.IFSTATEMENT
        del AST.WHILESTATEMENT
        del AST.EXPR
        del AST.BLOCK
        del AST.FACTOR
        del AST.PRIMARY
        del AST.NUMBER
        del AST.STRING
        del AST.IDENTIFIER
        del AST.OP
        del AST.EOL
        del AST.PUNCT
        del AST.EMPTY
        del AST.LEAF

    def __str__(self):
        return f"<{self.type} , {self.value}>"


    def eval_leaf(self,env:Environment):
        token = self.value
        if token.type == Token.IDENTIFIER:
            try:
                return env[token.value]
            except:
                return None
        elif token.type == Token.STRING:
            return token.value
        elif token.type == Token.NUMBER:
            return float(token.value)

    def eval_program(self,env:Environment):
        c = self.children[0]
        return c.eval(env)

    def eval_statement(self,env:Environment):
        c = self.children[0]
        return c.eval(env)

    def eval_statements(self,env:Environment):
        r = None
        for c in self.children:
            if c.type == AST.STATEMENT:
                r = c.eval(env)
            elif c.type == AST.LEAF:
                pass
            elif c.type == AST.STATEMENTS and c.children[0].type != AST.EMPTY:
                return c.eval(env)
        return r
    # def eval_primary(self,env:Environment):
    #     if len(self.children) == 3:
    #         return self.children[1].eval(env)
    #     else:
    #         return self.children[0].eval(env)

    def eval_factor(self,env:Environment):
        if len(self.children) == 1:
            return self.children[0].eval(env)
        elif len(self.children) == 2:
            return - self.children[1].eval(env)
    def eval_expr(self,env:Environment):
        if len(self.children) == 3:
            if type(self.children[0].value) == Token and  self.children[0].value.value == "(":
                return self.children[1].eval(env)

            op = self.children[1].value.value

            if op == "=":
                try:
                    token = self.children[0].children[0].value
                    if token.type == Token.IDENTIFIER:
                        b = self.children[2].eval(env)
                        env[token.value] = b
                        return b
                except:
                    raise Exception("[!] can only assign value to a variable.")

            a = self.children[0].eval(env)
            b = self.children[2].eval(env)

            if op == "+":
                return a + b
            elif op == "-":
                return a - b
            elif op == "*":
                return a * b
            elif op == "/":
                return a / b
            elif op == "<":
                return a < b
            elif op == ">":
                return a > b

        elif len(self.children) == 1:
            return self.children[0].eval(env)

    def eval_block(self,env:Environment):
        return self.children[1].eval(env)

    def eval_ifstatement(self,env:Environment):
        if len(self.children) == 5:
            e = self.children[1].eval(env)
            if e:
                return self.children[2].eval(env)
            else:
                return self.children[4].eval(env)
        elif len(self.children) == 3:
            e = self.children[1].eval(env)
            if e:
                return self.children[2].eval(env)
            else:
                return None
    def eval_whilestatement(self,env:Environment):
        e = self.children[1].eval(env)
        r = None
        while e:
            r = self.children[2].eval(env)
        return r
    def eval(self,env:Environment):
        if self.type == AST.LEAF:
            return self.eval_leaf(env)
        if self.type == AST.PROGRAM:
            return self.eval_program(env)
        if self.type == AST.STATEMENT:
            return self.eval_statement(env)
        if self.type == AST.STATEMENTS:
            return self.eval_statements(env)
        # if self.type == AST.PRIMARY:
        #     return self.eval_primary(env)
        if self.type == AST.FACTOR:
            return self.eval_factor(env)
        if self.type == AST.EXPR:
            return self.eval_expr(env)
        if self.type == AST.BLOCK:
            return self.eval_block(env)
        if self.type == AST.IFSTATEMENT:
            return self.eval_ifstatement(env)
        if self.type == AST.WHILESTATEMENT:
            return self.eval_whilestatement(env)
