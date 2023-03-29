from scanner import Scanner
from tokenType import TokenType
from token import Token

class Interpreter:
    def __init__(self) -> None:
        self.errors = False

                
    def fileExecute(self, file):
        
        with open(file, 'r') as file:
            lines = file.readlines()

        self.execute(lines)        

        if self.errors:
            sys.exit()        

    def executePrompt(self):
        lines = []
        while True:
            try:
                line = input('MyPromt>>> ')
                lines.append(line)
            except EOFError:
                break
            if not line:
                continue 
            self.execute(lines)

    def error(self, line, msg):
        self.report(f'{line} {msg}')

    def report(self, msg, location='', line=''):
        print(f'[line {line}] | Error {location}: {msg}')
        pass

    def execute(self, source):
        self.scanner = Scanner(source)
        self.tokens = self.scanner.tokensScan()

        for token in self.tokens:
            print(token)    
    