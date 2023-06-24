class SymbolsTable:
    def __init__(self):
        self.values = {}

    def existsIdentifier(self, identifier):
        return identifier in self.values

    def get(self, identifier):
        if self.existsIdentifier(identifier):
            return self.values[identifier]
        raise RuntimeError(f'Variable no definida {identifier}')

    def asign(self, identifier, value):
        self.values[identifier] = value