from dl.visitor import ASTVisitor
from dl.symbols import SymbolTable, VariableSymbol, ArgumentSymbol, ArraySymbol, FunctionSymbol
from dl.ast import Variable, ArrayIndex

class DLSemanticAnalyzer(ASTVisitor):
    """Run semantic analysis on an AST.

    Traverse an abstract syntax tree (AST) with recursive descent, and
    analyze each node to check that all symbols are declared, and
    types are checked.

    Attributes:
        st -- symbol table for the program
    """
    def __init__(self):
        self.st = SymbolTable()

    def analyze(self, program):
        """Begin semantic analysis on the top-level node."""
        self.visit(program)
        return program

    def visit_Integer(self, node):
        """Call the semantic analyzer for Integer AST nodes."""
        node.set_itype('int')

    def visit_Variable(self, node):
        """Call the semantic analyzer for Variable AST nodes."""
        # look up the node.name in the symbol table
        symbol = self.st.find_symbol(node.name) # symbol name
        # if the symbol is found check if the returned symbol is a VariableSymbol or an ArgumentSymbol
        if symbol and (isinstance(symbol, VariableSymbol) or isinstance(symbol, ArgumentSymbol)):
            # set inferred type of the node to the symbol.type
            node.set_itype('int')
        else:
            raise UndeclaredVariableError("Symbol not found or just isn't a VariableSymbol or ArgumentSymbol")

    def visit_ArrayIndex(self, node):
        """Call the semantic analyzer for ArrayIndex AST nodes."""
        # lookup the node.var.name in the symbol table
        symbol = self.st.find_symbol(node.var.name)
        # if the symbol is found and its an array symbol
        if symbol and isinstance(symbol, ArraySymbol):
            node.set_itype(symbol.type)
        else:
            raise UndeclaredVariableError("Symbol not found or just isn't an ArraySymbol")

    # same as visit_assignOp
    def visit_BinOp(self, node):
        """Call the semantic analyzer for BinOp AST nodes."""
        self.visit(node.left)
        self.visit(node.right)

        # Check the types of the two arguments.
        if (node.left.itype == 'int') and (node.right.itype == 'int'):
            node.set_itype('int')
        else:
            raise TypeCheckError("Type of arguments to binary operator should be 'int': " + node.op)

    def visit_RelOp(self, node):
        """Call the semantic analyzer for RelOp AST nodes."""
        self.visit(node.left)
        self.visit(node.right)

        # Check the types of the two arguments.
        valid_types = ['int', 'bool']
        if (node.left.itype in valid_types) and (node.right.itype in valid_types):
            node.set_itype('bool')
        else:
            raise TypeCheckError("Types of arguments to relational operator should be 'int' or 'bool': " + node.op)

    def visit_FunctionCall(self, node):
        """Call the semantic analyzer for FunctionCall AST nodes."""
        # look up the node.name in the symbol table
        nodeName = self.st.find_symbol(node.name)
        # if the symbol is found
        if nodeName and isinstance(nodeName, FunctionSymbol):
            node.set_itype('int')
        else:
            raise UndeclaredFunctionError("Symbol not found, or the symbol isn't a FunctionSymbol")
        # node.args might be undefined so first instantiate a count variable to zero and compare
        count = 0
        if node.args:
            count = node.args.count()
            self.visit(node.args)
        if count != nodeName.args:
            raise UndeclaredFunctionError("Number of arguments in the function call isn't the same ")

    def visit_Arguments(self, node):
        """Call the semantic analyzer for Arguments AST nodes."""
        for argument in node.arguments:
            self.visit(argument)

    def visit_Assign(self, node):
        """Call the semantic analyzer for Assign AST nodes."""
        self.visit(node.left)
        self.visit(node.right)

        # Check the types of the two arguments.
        if node.left.itype == 'int' and node.right.itype == 'int':
            node.set_itype('int')
        else:
            raise TypeCheckError("Type of arguments to assignment should be 'int': " + node.op)

    def visit_Print(self, node):
        """Call the semantic analyzer for Print AST nodes."""
        self.visit(node.arg)

    def visit_Read(self, node):
        """Call the semantic analyzer for Read AST nodes."""
        self.visit(node.result)

    def visit_Return(self, node):
        """Call the semantic analyzer for Return AST nodes."""
        self.visit(node.result)

    def visit_If(self, node):
        """Call the semantic analyzer for If AST nodes."""
        self.visit(node.condition)
        self.visit(node.body_true)
        self.visit(node.body_else)

    def visit_While(self, node):
        """Call the semantic analyzer for While AST nodes."""
        self.visit(node.condition)
        self.visit(node.body)

    def visit_Block(self, node):
        """Call the semantic analyzer for Block AST nodes."""
        for statement in node.statements:
            self.visit(statement)

    def visit_Declarations(self, node):
        """Call the semantic analyzer for Declarations AST nodes."""
        for declaration in node.declarations:
            self.visit(declaration)

    def visit_VariableDeclarations(self, node):
        """Call the semantic analyzer for VariableDeclarations AST nodes."""
        symbol_type = node.var_type.lower()
        # iterate through node.variables
        for variable in node.variables:
            # check if the type of each declaration is 'variable' or 'arrayindex'
            if isinstance(variable, Variable):
                # if the declaration is a variable, add symbol to the symbol table
                self.st.add_var_symbol(variable.name, 'int')
            elif isinstance(variable, ArrayIndex):
                # if the declaration is an ArrayIndex, add a symbol to the symbol table
                self.st.add_array_symbol(variable.var.name, 'int', variable.index)
            else:
                raise TypeCheckError("declaration isn't a variable or array index")

    def visit_FunctionDeclaration(self, node):
        """Call the semantic analyzer for FunctionDeclaration AST nodes."""

        arg_count = 0
        if node.args:
            arg_count = node.args.count()
        # add a symbol to the symbol table for the function
        self.st.add_func_symbol(node.name, arg_count)
        # create a new scope in the symbol table for the function
        self.st.enter_scope()
        # iterate through the args, and add each one to the symbol table
        if node.args: # ensure node.args exists
            for argument in node.args.arguments:
                self.st.add_arg_symbol(argument.name, ArgumentSymbol)
        # if there are any variable declarations for the function
        if node.vars:
            self.visit(node.vars)
        self.visit(node.body)
        # exit the scope for the function
        self.st.exit_scope()

    def visit_Program(self, node):
        """Call the semantic analyzer for Program AST nodes."""
        self.st.enter_scope()
        if node.declarations:
            self.visit(node.declarations)
        self.visit(node.body)
        self.st.exit_scope()

class SemanticError(Exception):
    """Exception raised for errors detected in semantic analysis.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class UndeclaredVariableError(SemanticError):
    """Exception raised for use of undeclared variables."""


class UndeclaredFunctionError(SemanticError):
    """Exception raised for use of undeclared function."""



class TypeCheckError(SemanticError):
    """Exception raised for type errors."""

