class Expression:
    """Base class for all expression nodes.

    Attributes:
        none
    """
    pass

class Integer(Expression):
    """Integer constant node.

    Attributes:
        value -- the integer value of the node
    """
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Integer(%s)" % (self.value)

class Variable(Expression):
    """Variable identifier node.

    Attributes:
        name -- the variable name
    """
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Variable(%s)" % (self.name)

class ArrayIndex(Expression):
    """Array index node, for both read and write.

    Attributes:
        name -- the array variable name
        index -- the array element to read or write
    """
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __repr__(self):
        return "ArrayIndex(%s, %s)" % (self.name, self.index)

class BinOp(Expression):
    """Binary operator node.

    Attributes:
        op -- the type of the binary operator
        left -- the left-side argument to the operator
        right -- the right-side argument to the operator
    """
    def __init__(self, op, left=None, right=None):
        self.op = op
        self.left = left
        self.right = right

    def set_left(self, left):
        """Set the left-side argument of the operator"""
        self.left = left

    def set_right(self, right):
        """Set the right-side argument of the operator"""
        self.right = right

    def __repr__(self):
        return "BinOp(%s, %s, %s)" % (self.op, self.left, self.right)

class RelOp(BinOp):
    """Relational operator node.

    Attributes:
        op -- the type of the binary operator
        left -- the left-side argument to the operator
        right -- the right-side argument to the operator
    """
    def __repr__(self):
        return "RelOp(%s, %s, %s)" % (self.op, self.left, self.right)

class FunctionCall(Expression):
    """Function call node.

    Attributes:
        name -- the function name
        args -- a list of arguments to pass to the function (optional)
    """
    def __init__(self, name, args=None):
        self.name = name
        self.args = args

    def __repr__(self):
        if self.args:
            return "FunctionCall(%s, %s)" % (self.name, self.args)
        else:
            return "FunctionCall(%s)" % (self.name)

class Arguments():
    """Node for a sequence of arguments to a function, in order.

    Attributes:
        arguments -- an ordered list of arguments
    """
    def __init__(self, argument=None):
        if argument:
            self.arguments = [argument]
        else:
            self.arguments = []

    def prepend(self, argument):
        """Add an argument to the beginning of the argument list."""
        self.arguments.insert(0, argument)

    def __repr__(self):
        display = "Arguments(" + ", ".join(map(str, self.arguments)) + ")"
        return display

class Statement:
    """Base class for all statement nodes.

    Attributes:
        none
    """
    pass

class Assign(Statement):
    """Assignment statement node.

    Attributes:
        left -- the variable or array element to assign to
        right -- the value to be assigned
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "Assign(%s, %s)" % (self.left, self.right)

class Print(Statement):
    """Print statement node.

    Attributes:
        arg -- the single argument to print
    """
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        return "Print(%s)" % (self.arg)

class Read(Statement):
    """Read statement node.

    Attributes:
        result -- the variable to store the read value
    """
    def __init__(self, result):
        self.result = result

    def __repr__(self):
        return "Read(%s)" % (self.result)

class Return(Statement):
    """Return statement node.

    Attributes:
        result -- the result to return
    """
    def __init__(self, result):
        self.result = result

    def __repr__(self):
        return "Return(%s)" % (self.result)

class If(Statement):
    """If statement node.

    Attributes:
        condition -- the condition of the 'if'
        body_true -- the block to run if the condition is true
        body_else -- the block to run if the condition is false (optional)
    """
    def __init__(self, condition, body_true, body_else=None):
        self.condition = condition
        self.body_true = body_true
        self.body_else = body_else

    def __repr__(self):
        if self.body_else:
            return "If(%s, %s, %s)" % (self.condition, self.body_true, self.body_else)
        else:
            return "If(%s, %s)" % (self.condition, self.body_true)

class While(Statement):
    """While statement node.

    Attributes:
        condition -- the condition of the loop
        body -- the body of the loop
    """
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return "While(%s, %s)" % (self.condition, self.body)

class Block():
    """Node for a sequence of statements, in order.

    Attributes:
        statements -- an ordered list of statements
    """
    def __init__(self, statement=None):
        if statement:
            self.statements = [statement]
        else:
            self.statements = []

    def prepend(self, statement):
        """Add a statement to the beginning of the statement list."""
        self.statements.insert(0, statement)

    def __repr__(self):
        display = "Block(" + ", ".join(map(str, self.statements)) + ")"
        return display

class Declarations():
    """Node for a sequence of declarations, in order.

    Attributes:
        declarations -- an ordered list of declarations
    """
    def __init__(self, declaration=None):
        if declaration:
            self.declarations = [declaration]
        else:
            self.declarations = []

    def prepend(self, declaration):
        """Add a declaration to the beginning of the declaration list."""
        self.declarations.insert(0, declaration)

    def __repr__(self):
        display = "Declarations(" + ", ".join(map(str, self.declarations)) + ")"
        return display

class VariableDeclarations():
    """Node for a sequence of variable declarations, in order.

    Attributes:
        var_type -- the type of the variables
        variables -- an ordered list of variables to declare
    """
    def __init__(self, variable=None):
        self.var_type = None
        if variable:
            self.variables = [variable]
        else:
            self.variables = []

    def set_type(self, var_type):
        """Set the variable type for the declaration list."""
        self.var_type = var_type

    def prepend(self, variable):
        """Add a variable to the beginning of the declaration list."""
        self.variables.insert(0, variable)

    def __repr__(self):
        display = "VariableDeclarations(%s, " % (self.var_type)
        display += ", ".join(map(str, self.variables))
        display += ")"
        return display

class FunctionDeclaration(Expression):
    """Function declaration node.

    Attributes:
        name -- the function name
        body -- the body of the function
        args -- a list of arguments to be passed to the function (optional)
        vars -- a list of other variables to declare for the function (optional)
    """
    def __init__(self, name, args=None):
        self.name = name
        self.args = args
        self.body = None
        self.vars = None

    def set_body(self, data):
        """Set the body, and optionally the var list for the function declaration.

        Takes a single argument, which is a dictionary with one or two keys:

            temporary = {'body': p.block}
            node.set_body(temporary)

        or

            temporary = {'body': p.block, 'vars': p.variabledeclaration}
            node.set_body(temporary)
        """
        if type(data) is dict:
            if 'body' in data:
                self.body = data['body']
            if 'vars' in data:
                self.vars = data['vars']

    def __repr__(self):
        if self.args and self.vars:
            return "FunctionDeclaration(%s, %s, %s, %s)" % (self.name, self.args, self.vars, self.body)
        elif self.args:
            return "FunctionDeclaration(%s, %s, %s)" % (self.name, self.args, self.body)
        elif self.vars:
            return "FunctionDeclaration(%s, %s, %s)" % (self.name, self.vars, self.body)
        else:
            return "FunctionDeclaration(%s, %s)" % (self.name, self.body)

class Program():
    """Top-level node for a program.

    Attributes:
        body -- the body of the program
        declarations -- an ordered list of declarations (optional)
    """
    def __init__(self, body, declarations=None):
        self.body = body
        self.declarations = declarations

    def __repr__(self):
        if self.declarations:
            return "Program(%s, %s)" % (self.declarations, self.body)
        else:
            return "Program(%s)" % (self.body)
