import sys


class SymbolsTable:
    def __init__(self):
        self.values = {}

    def existsIdentifier(self, key):
        if key in self.values.keys():
            return True
        return False

    def get(self, key):
        print(key)
        if self.existsIdentifier(key):
            return self.values[key]
        else:
            print(f"Variable {key} no definida")
            sys.exit()

    def asign(self, key, value):
        if self.existsIdentifier(key):
            self.values[key]=value
            return
        else:
            self.values.__setitem__(key,value)
            return

    def reasign(self, key, value):
        self.values[key]=value
        return

def init():
    global symbols
    symbols = SymbolsTable() 