from tokens import Token

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
        # del AST.EMPTY
        del AST.BLOCK
        del AST.FACTOR
        del AST.PRIMARY
        del AST.NUMBER
        del AST.STRING
        del AST.IDENTIFIER
        # del AST.LEAF
        del AST.OP
        del AST.EOL
        del AST.PUNCT

    def __str__(self):
        return f"<{self.type} , {self.value}>"

