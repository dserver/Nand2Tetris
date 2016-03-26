
class SymbolTable:
    table = dict()
    def addEntry(self, symbol, address):
        self.table[symbol] = address

    def contains(self, symbol):
        return self.table.has_key(symbol)

    def getAddress(self, symbol):
        if self.table.has_key(symbol):
            return self.table.get(symbol)