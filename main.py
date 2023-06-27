from interpreterr import Interpreter
from symbolsTable import init
import sys

def main():
    interpreter = Interpreter()

    if len(sys.argv) > 2:
        print('Uso: interpreter [script]')
        sys.exit()
    if len(sys.argv) == 2:
        interpreter.fileExecute(sys.argv[1])
    else:
        interpreter.executePrompt()


if __name__ == '__main__':
    main()    