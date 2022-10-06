from lexer import Lexer
from syntax import Syntax
from ast import AST
code = '''if a {
    1+2;
}else{
    7*7
}'''
lexer = Lexer(code=code)
# lexer.display()

syntax = Syntax()
AST.debug()
ast = syntax.parse(lexer)

# print(ast)
