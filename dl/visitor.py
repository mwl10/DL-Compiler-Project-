class ASTVisitor:
    """Generic base class for visitor pattern.

    Classes that traverse the AST inherit from this base class.
    """
    def visit(self, node):
        """Call the generator for the node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.missing)
        return visitor(node)

    def missing(self, node):
        """Called if no explicit generator exists for a node."""
        raise VisitorDefinitionError("No visitor defined for nodes of type: " + node.__class__.__name__)

class VisitorDefinitionError(Exception):
    """Exception raised for missing visitor methods.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
