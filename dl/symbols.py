class SymbolTable:
    """Class for managing program symbols

    Attributes:
        scopes -- a tree of nested scopes
        current -- the current scope object
    """
    def __init__(self):
        self.current = None
        self.scopes = None

    def enter_scope(self):
        """Start a new scope"""
        parent = self.current
        new_scope = Scope(parent)
        self.current = new_scope

        # Store the top node of the nested scopes
        if parent is None:
            self.scopes = new_scope

    def exit_scope(self):
        """Leave current scope"""
        parent = self.current.parent
        self.current = parent

    def add_var_symbol(self, symbol_name, symbol_type):
        """Add a variable symbol to the current scope"""
        symbol = VariableSymbol(symbol_name, symbol_type)
        self.current.add_symbol(symbol)

    def add_arg_symbol(self, symbol_name, symbol_type):
        """Add an argument symbol to the current scope"""
        symbol = ArgumentSymbol(symbol_name, symbol_type)
        self.current.add_symbol(symbol)

    def add_array_symbol(self, symbol_name, symbol_type, size):
        """Add an array symbol to the current scope"""
        symbol = ArraySymbol(symbol_name, symbol_type, size)
        self.current.add_symbol(symbol)

    def add_func_symbol(self, symbol_name, size):
        """Add a function symbol to the current scope"""
        symbol = FunctionSymbol(symbol_name, size)
        self.current.add_symbol(symbol)

    def find_symbol(self, symbol_name):
        """Search for symbol

	Search current scope first, then outer scopes. Return the
        first symbol found, or false if the symbol is not found.
        """
        return self.current.find_symbol(symbol_name)

    def check_local(self, symbol_name):
        """Check if symbol is defined in the current scope"""
        symbol = self.current.get_symbol(symbol_name)
        if symbol:
            return True
        else:
            return False

class Scope:
    """A single scope in the symbol table.

    Attributes:
        symbols -- storage for symbols, indexed by name
        parent -- the parent scope of the current scope, if any
        scopes -- any nested scopes within the current scope
    """
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}

    def add_symbol(self, symbol):
        """Add a symbol to the scope"""
        self.symbols[symbol.name] = symbol

    def get_symbol(self, symbol_name):
        """Retrieve a symbol from the scope"""
        if symbol_name in self.symbols:
            return self.symbols[symbol_name]
        else:
            return False

    def find_symbol(self, symbol_name):
        """Search for symbol

	Search current scope first, then outer scopes. Return the
        first symbol found, or false if the symbol is not found.
        """
        search_scope = self
        while search_scope is not None:
            # Iterate through all the parent scopes, looking for the
            # symbol in each one, until it is found.
            symbol = search_scope.get_symbol(symbol_name)
            if symbol:
                return symbol
            else:
                parent_scope = search_scope.parent
                search_scope = parent_scope

        # No symbol was found in any parent scope.
        return False

class VariableSymbol:
    """A variable symbol in the symbol table.

    Attributes:
        name -- the name of the symbol
        type -- the type of the symbol
    """
    def __init__(self, name, symbol_type):
        self.name = name
        self.type = symbol_type

class ArgumentSymbol:
    """An argument symbol in the symbol table.

    Attributes:
        name -- the name of the symbol
        type -- the type of the symbol
    """
    def __init__(self, name, symbol_type):
        self.name = name
        self.type = symbol_type

class ArraySymbol:
    """An array symbol in the symbol table.

    Attributes:
        name -- the name of the symbol
        type -- the type of the elements in the array
        size -- the size of the array
    """
    def __init__(self, name, element_type, size):
        self.name = name
        self.type = element_type
        self.size = size

class FunctionSymbol:
    """A function symbol in the symbol table.

    Attributes:
        name -- the name of the symbol
        args -- how many arguments are required by the function
    """
    def __init__(self, name, arg_count):
        self.name = name
        self.args = arg_count
