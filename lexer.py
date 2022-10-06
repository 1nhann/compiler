from collections import deque
from tokens import Token
import re

class Lexer:
    EOL = Token(Token.EOL,"\\n")
    EOF = Token(Token.EOF,"\x00")
    PATTERN = f"{Token.PATTERNS['space']}(({Token.PATTERNS['comment']})|({Token.PATTERNS['number']})|({Token.PATTERNS['string']})|({Token.PATTERNS['identifier']})|({Token.PATTERNS['operator2']})|({Token.PATTERNS['operator']})|({Token.PATTERNS['punct']}))?"

    def __init__(self,code:str):
        self.code = code
        self.queue = deque()
        self.gc = deque()

    def fill_queue(self):
        lines = self.code.split("\n")
        for line in lines:
            s = line
            start = 0
            while start <= len(s) - 1:
                s = s[start:]
                m = re.match(Lexer.PATTERN, s)
                start = m.end()
                self.add_token(matcher=m)
            self.queue.append(Lexer.EOL)
        self.queue.append(Lexer.EOF)

    def next(self):
        if self.code == '':
            return Lexer.EOF

        i = self.code.find("\n")
        line = ""
        if i == -1:
            line = self.code
        elif i == 0:
            self.code = self.code[1:]
            return Lexer.EOL
        else:
            line = self.code[:i]

        m = re.match(Lexer.PATTERN, line)
        start = m.end()
        self.code = self.code[start:]
        if self.add_token(matcher=m):
            return self.queue.pop()
        else:
            return self.next()

    def add_token(self,matcher):
        if matcher == None:
            raise Exception("[!] Error !!!")
        g = matcher.groups()
        if g[1] != None:
            return False # comment
        elif g[3] != None and g[4] != None:
            self.queue.append(Token(Token.STRING,g[4]))
        elif g[2] != None:
            self.queue.append(Token(Token.NUMBER,g[2]))
        elif g[7] != None or g[8] != None:
            self.queue.append(Token(Token.OP,g[7] if g[7] != None else g[8]))
        elif g[9] != None:
            self.queue.append(Token(Token.PUNCT,g[9]))
        else:
            self.queue.append(Token(Token.IDENTIFIER,g[0]))
        return True

    def read(self) -> Token:
        if(len(self.queue) == 0):
            self.fill_queue()
        t = self.queue.popleft()
        self.gc.append(t)
        return t

    def unread(self):
        if(len(self.gc) > 0):
            t = self.gc.pop()
            self.queue.appendleft(t)
            return t

    def peek(self) -> Token:
        if(len(self.queue) == 0):
            self.fill_queue()
        return self.queue[0]

    def display(self):
        t = self.next()
        while t != Lexer.EOF:
            print(">>> " + str(t))
            t = self.next()