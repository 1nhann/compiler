from lexer import Lexer
from syntax import Syntax
from interpreter import Interpreter
code = '''a = 1 > 0
if a {
    7 * 8
}else{
    2 + 3
}'''
lexer = Lexer(code=code)
# lexer.display()

syntax = Syntax()
ast = syntax.parse(lexer)

inter = Interpreter(ast)

r = inter.run()
print(r)