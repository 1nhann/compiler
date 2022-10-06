class Token:
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    OP = "OP"
    PUNCT = "PUNCT"
    EOL = "EOL"
    EOF = "EOF"

    PATTERNS = {
        "number": "[0-9]+",
        "identifier": "[A-Za-z_][A-Za-z0-9_]*",
        "string": r'"((\\|"|\n|[^"])*)"',
        "comment": "//.*",
        "space": r"\s*",
        "operator2": r"==|<=|>=|&&|\|\|",
        "operator": r"\+|-|\*|/|<|>|=",
        "punct": r"\(|\)|\{|\}|;"
    }

    def __init__(self,type:str,value:str):
        self.type = type
        self.value = value

    def __str__(self):
        return str((self.type,self.value))

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value