import scanner
import tokenType
import token
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
                line = input('MyPromt>>> ')
                lines.append(line)
            except EOFError:
                break
            if not line:
                continue 
            self.execute(lines)

    def error(self, line, msg):
        self.report(f'{line} {msg}')

    def report(self, line, location, msg):
        print(f'[line {line}] | Error {location}: {msg}')
        pass


    def execute(self, source):
        self.scanner = scanner.Scanner(source)
        self.tokens = self.scanner.tokensScan()

        for token in self.tokens:
            print(token)




def main():
    interprete = Interpreter()

    if len(sys.argv) > 2:
        print('Uso: interprete [script]')
        sys.exit()
    if len(sys.argv) == 2:
        interprete.fileExecute(sys.argv[1])
    else:
        interprete.executePrompt()


if __name__ == '__main__':
    main()    
    
    