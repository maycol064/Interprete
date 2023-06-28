from scanner import Scanner
from parserr import Parser
from postfixedGenerator import Postfixed
from generatorATS import GeneratorAST
import sys

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
                line = input('Enter promt $ > ')
                lines.append(line)
            except EOFError:
                break
            if not line:
                continue 
            self.execute(lines)

    def error(line, msg):
        print(f'[line {line}] | {msg}')
        pass

    def execute(self, source):
        self.scanner = Scanner(source)
        self.tokens = self.scanner.scanTokens()
        # for t in self.tokens:
        #     print(t)
        self.parser = Parser(self.tokens)
        isValid = self.parser.parse()
        # print(isValid)
        self.postfixed = Postfixed(self.tokens)
        resPostfixed = self.postfixed.convert()
        # for p in resPostfixed:
        #     print(p)
        self.generateAST = GeneratorAST(resPostfixed)
        self.program = self.generateAST.generateAST()
        self.program.iterate()
        

    