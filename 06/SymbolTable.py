
class SymbolTable:

    symbol_table = []
    location_counter = 0

    def __init__():
        pass

    def update(self, sym=None):
        if (sym is None):
            self.location_counter += 1
        else
            self.symbol_table.append((sym, self.location_counter))
