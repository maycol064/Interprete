import sys


class SymbolsTable:
    def __init__(self):
        self.values = {}

    def existsIdentifier(self, identifier):
        return identifier in self.values

    def get(self, identifier):
        print(identifier)
        if self.existsIdentifier(identifier):
            return self.values[identifier]
        else:
            print(f"{identifier} no está definida")
            sys.exit()

    def asign(self, id, value):
        if self.existsIdentifier(id):
            self.values[id] = value
            return
        else:
            self.values.__setitem__(id, value)
            return
        raise Exception(f"{id} no está definida")

    def reasign(self, id, value):
        self.valuess[id] = value
        return

def init():
    global symbols
    symbols = SymbolsTable() 