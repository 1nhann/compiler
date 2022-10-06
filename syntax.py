from lexer import Lexer
from ast import AST
from tokens import Token
from collections import deque


class Parser:
    def __init__(self,type:str):
        self.type = type
        self.or_parsers = []
        self.and_parsers = []

    def aanndd(self,parser):
        self.and_parsers.append(parser)
        return self

    def first(self,parser):
        self.and_parsers.append(parser)
        return self

    def oorr(self,parser):
        self.or_parsers.append(parser)
        return self

    def rollback(self,ast:AST,lexer:Lexer):
        q = deque()
        q.append(ast)
        count = 0
        while len(q):
            a = q.popleft()
            if a.type == AST.LEAF:
                count += 1
            for c in a.children:
                q.append(c)
        for i in range(count):
            lexer.unread()

    def parse(self,lexer:Lexer):
        ast = AST(self.type, None)
        if self.type == AST.EMPTY:
            return ast

        if len(self.and_parsers):
            for parser in self.and_parsers:
                a = parser.parse(lexer)
                if a:
                    ast.add_child(a)
                else:
                    self.rollback(ast,lexer)
                    return None
        elif len(self.or_parsers):
            for parser in self.or_parsers:
                a = parser.parse(lexer)
                if a:
                    if a.type != "SEQUENCE":
                        ast.add_child(a)
                    else:
                        ast.set_children(a.children)
                    return ast
            self.rollback(ast, lexer)
            return None
        elif lexer.peek().type == self.type:
            ast.value = lexer.read()
            ast.type = AST.LEAF
        else:
            return None

        return ast

class TokenP(Parser):
    def __init__(self,token:Token):
        self.token = token
        super().__init__(self.token.type)
    def parse(self,lexer:Lexer):
        if lexer.peek() == self.token:
            lexer.read()
            return AST(AST.LEAF,self.token)
        else:
            return None

class Punct(TokenP):
    def __init__(self,char:str):
        super().__init__(Token(Token.PUNCT,char))

class Char(TokenP):
    def __init__(self,char:str):
        if char == "-":
            super().__init__(Token(Token.OP,"-"))
        else:
            super().__init__(Token(Token.IDENTIFIER,char))

class Sequence(Parser):
    def __init__(self):
        super().__init__("SEQUENCE")

class Syntax:
    """
    PRIMARY => (EXPR)|NUMBER|IDENTIFIER|STRING

    FACTOR => - PRIMARY | PRIMARY

    EXPR => FACTOR OP FACTOR
            | FACTOR

    STATEMENTS => STATEMENT EOL STATEMENTS
                | STATEMENT ; STATEMENTS
                | EMPTY

    BLOCK => { STATEMENTS }

    IFSTATEMENT => if EXPR BLOCK else BLOCK
                | if EXPR BLOCK

    WHILESTATEMENT => while EXPR BLOCK

    STATEMENT => IFSTATEMENT | WHILESTATEMENT | EXPR | EMPTY

    PROGRAM => STATEMENTS EOF
    """
    def __init__(self):
        number = Parser(AST.NUMBER)
        identifier = Parser(AST.IDENTIFIER)
        string = Parser(AST.STRING)
        op = Parser(AST.OP)
        eol = TokenP(Lexer.EOL)
        eof = TokenP(Lexer.EOF)
        expr0 = Parser(AST.EXPR)

        primary = Parser(AST.PRIMARY).oorr(
           Sequence().first(Punct("(")).aanndd(expr0).aanndd(Punct(")"))
        ).oorr(
            number
        ).oorr(
            identifier
        ).oorr(
            string
        )

        factor = Parser(AST.FACTOR).oorr(
            Sequence().first(Char("-")).aanndd(number)
        ).oorr(primary)

        expr = expr0.oorr(
            Sequence().first(factor).aanndd(op).aanndd(factor)
        ).oorr(factor)

        if_statement0 = Parser(AST.IFSTATEMENT)
        while_statement0 = Parser(AST.WHILESTATEMENT)

        statement = Parser(AST.STATEMENT).oorr(
            if_statement0
        ).oorr(
            while_statement0
        ).oorr(
            expr
        ).oorr(
            Parser(AST.EMPTY)
        )

        statements0 = Parser(AST.STATEMENTS)

        statements = statements0.oorr(
            Sequence().first(statement).aanndd(eol).aanndd(statements0)
        ).oorr(
            Sequence().first(statement).aanndd(Punct(";")).aanndd(statements0)
        ).oorr(
            Parser(AST.EMPTY)
        )

        block = Parser(AST.BLOCK).first(Punct("{")).aanndd(statements).aanndd(Punct("}"))

        if_statement = if_statement0.oorr(
            Sequence().first(Char("if")).aanndd(expr).aanndd(block).aanndd(Char("else")).aanndd(block)
        ).oorr(
            Sequence().first(Char("if")).aanndd(expr).aanndd(block)
        )

        while_statement = while_statement0.first(Char("while")).aanndd(expr).aanndd(block)

        self.program = Parser(AST.PROGRAM).first(statements).aanndd(eof)


    def parse(self,lexer:Lexer):
        return self.program.parse(lexer)