from astree import AST,Environment

class Interpreter:
    def __init__(self,program:AST):
        self.program = program
    def run(self):
        env = Environment()
        return self.program.eval(env)

