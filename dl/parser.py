# -----------------------------------------------------------------------------
# parser.py
# -----------------------------------------------------------------------------

import sys
sys.path.append('.')

from sly import Parser
from dl.lexer import DLLexer
from dl.ast import Integer, Variable, BinOp, RelOp, ArrayIndex, \
                   Assign, Print, Read, Return, If, While, Block, \
                   FunctionCall, Arguments, FunctionDeclaration, \
                   Declarations, VariableDeclarations, Program

class DLParser(Parser):
    """LALR parser for simple DL language."""
    tokens = DLLexer.tokens

    precedence = (
        # Lowest
        ('left', EQOP, NEOP, LEOP, LTOP, GEOP, GTOP),
        ('left', PLUSOP, MINUSOP),
        ('left', MULTIPLYOP, DIVIDEOP),
        # Highest
        )

    # <program> ::= <block>
    #             | <declarations> <block>

    @_('block')
    def program(self, p):
        """Implement the <program> production alternate without declarations."""
        return Program(p.block)

    @_('declarations block')
    def program(self, p):
        """Implement the <program> production alternate with declarations."""
        return Program(p.block, p.declarations)

    # <declarations> ::= <declaration>
    #                  | <declaration> <declarations>

    @_('declaration')
    def declarations(self, p):
        """Implement the <declarations> production alternate with a single <declaration>."""
        return Declarations(p.declaration)

    @_('declaration declarations')
    def declarations(self, p):
        """Implement the <declarations> production alternate for a sequence of <declaration>s."""
        node = p.declarations

        if p.declaration:
            node.prepend(p.declaration)

        return node

    # <declaration> ::= <variabledeclaration> | <functiondeclaration>

    @_('variabledeclaration')
    def declaration(self, p):
        """Implement the <declaration> production alternate for <variabledeclaration>."""
        return p.variabledeclaration

    @_('functiondeclaration')
    def declaration(self, p):
        """Implement the <declaration> production alternate for <functiondeclaration>."""
        return p.functiondeclaration

    # <variabledeclaration> ::= int <vardeflist> ;

    @_('INT vardeflist SEMICOLON')
    def variabledeclaration(self, p):
        """Implement the <variabledeclaration> production."""
        node = p.vardeflist
        node.set_type("INT")
        return node

    # <vardeflist> ::= <vardec> | <vardec> , <vardeflist>

    @_('vardec')
    def vardeflist(self, p):
        """Implement the <vardeflist> production alternate with a single <vardec>."""
        return VariableDeclarations(p.vardec)

    @_('vardec COMMA vardeflist')
    def vardeflist(self, p):
        """Implement the <vardeflist> production alternate with a sequence of <vardec>s."""
        node = p.vardeflist

        if p.vardec:
            node.prepend(p.vardec)

        return node

    # <vardec> ::= <identifier> | <identifier> [ <constant> ]

    @_('variable')
    def vardec(self, p):
        """Implement the <vardec> production alternate with a single variable."""
        return p.variable

    @_('variable OPENSQUARE constant CLOSESQUARE')
    def vardec(self, p):
        """Implement the <vardec> production alternate with an array."""
        return ArrayIndex(p.variable, p.constant)


    # <functiondeclaration> ::= <identifier> (); <functionbody>
    #                         | <identifier> ( <arglist> ); <functionbody>

    @_('IDENTIFIER OPENPAREN CLOSEPAREN SEMICOLON functionbody')
    def functiondeclaration(self, p):
        """Implement the <functiondeclaration> production alternate without arguments."""
        node = FunctionDeclaration(p.IDENTIFIER)
        #print(p.functionbody)
        node.set_body(p.functionbody)
        return node

    @_('IDENTIFIER OPENPAREN arglist CLOSEPAREN SEMICOLON functionbody')
    def functiondeclaration(self, p):
        """Implement the <functiondeclaration> production alternate with arguments."""
        node = FunctionDeclaration(p.IDENTIFIER, p.arglist)
        #print(p.functionbody)
        node.set_body(p.functionbody)
        return node

    # <functionbody> ::= <variabledeclaration> <block> | <block>

    @_('variabledeclaration block')
    def functionbody(self, p):
        """Implement the <functionbody> production alternate with variable declarations."""
        temporary = { 'vars': p.variabledeclaration, 'body': p.block }
        return temporary

    @_('block')
    def functionbody(self, p):
        """Implement the <functionbody> production alternate without variable declarations."""
        temporary = { 'body': p.block }
        return temporary

    # <arglist> ::= <identifier> | <identifier> , <arglist>

    @_('variable')
    def arglist(self, p):
        """Implement the <arglist> production alternate for a single argument."""
        return Arguments(p.variable)

    @_('variable COMMA arglist')
    def arglist(self, p):
        """Implement the <arglist> production alternate for a sequence of arguments."""
        node = p.arglist

        if p.variable:
            node.prepend(p.variable)

        return node

    # <block> ::= { <statementlist> }

    @_('OPENCURLY statementlist CLOSECURLY')
    def block(self, p):
        """Implement the <block> production."""
        return p.statementlist

    # <statementlist> ::= <statement> | <statement> ; <statementlist>

    @_('statement')
    def statementlist(self, p):
        """Implement the <statementlist> production alternate for a single <statement>."""
        return Block(p.statement)

    @_('statement SEMICOLON statementlist')
    def statementlist(self, p):
        """Implement the <statementlist> production alternate for a sequence of <statement>s."""
        node = p.statementlist

        if p.statement:
            node.prepend(p.statement)

        return node

    # <statement> ::= <assignment> | <ifstatement> | <whilestatement>
    #               | <block> | <printstatement> | <readstatement>
    #               | <returnstatement> | <empty>

    @_('assignment')
    def statement(self, p):
        """Implement the <statement> production alternate for <assignment>."""
        return p.assignment

    @_('ifstatement')
    def statement(self, p):
        """Implement the <statement> production alternate for <ifstatement>."""
        return p.ifstatement

    @_('whilestatement')
    def statement(self, p):
        """Implement the <statement> production alternate for <whilestatement>."""
        return p.whilestatement

    @_('block')
    def statement(self, p):
        """Implement the <statement> production alternate for a block as a statement."""
        return p.block

    @_('printstatement')
    def statement(self, p):
        """Implement the <statement> production alternate for <printstatement>."""
        return p.printstatement

    @_('readstatement')
    def statement(self, p):
        """Implement the <statement> production alternate for <readstatement>."""
        return p.readstatement

    @_('returnstatement')
    def statement(self, p):
        """Implement the <statement> production alternate for <returnstatement>."""
        return p.returnstatement

    @_('empty')
    def statement(self, p):
        """Implement the <statement> production alternate for <empty>."""
        pass

    # <assignment> ::= <identifier> = <expression>
    #                | <identifier> [ <expression> ] = <expression>

    @_('variable ASSIGNOP expression')
    def assignment(self, p):
        """Implement the <assignment> production alternate for single variable assignment."""
        return Assign(p.variable, p.expression)

    @_('variable OPENSQUARE expression CLOSESQUARE ASSIGNOP expression')
    def assignment(self, p):
        """Implement the <assignment> production alternate for array element assignment."""
        arrayindex = ArrayIndex(p.variable, p.expression0)
        return Assign(arrayindex, p.expression1)

    # <ifstatement> ::= if ( <bexpression> ) <block> else <block>
    #                 | if ( <bexpression> ) <block>

    @_('IF OPENPAREN bexpression CLOSEPAREN block ELSE block')
    def ifstatement(self, p):
        """Implement the <ifstatement> production alternate with an else block."""
        return If(p.bexpression, p.block0, p.block1)

    @_('IF OPENPAREN bexpression CLOSEPAREN block')
    def ifstatement(self, p):
        """Implement the <ifstatement> production alternate without an else block."""
        return If(p.bexpression, p.block)

    # <whilestatement> ::= while ( <bexpression> ) <block>

    @_('WHILE OPENPAREN bexpression CLOSEPAREN block')
    def whilestatement(self, p):
        """Implement the <whilestatement> production."""
        return While(p.bexpression, p.block)

    # <printstatement> ::= print ( <expression> )

    @_('PRINT OPENPAREN expression CLOSEPAREN')
    def printstatement(self, p):
        """Implement the <printstatement> production."""
        return Print(p.expression)

    # <readstatement> ::= read ( <identifier> )

    @_('READ OPENPAREN variable CLOSEPAREN')
    def readstatement(self, p):
        """Implement the <readstatement> production."""
        return Read(p.variable)

    # <returnstatement> ::= return <expression>

    @_('RETURN expression')
    def returnstatement(self, p):
        """Implement the <returnstatement> production."""
        return Return(p.expression)

    # <expression> ::= <expression> <addingop> <term>
    #                | <term> | <addingop> <term>
    # <addingop> ::= + | -

    @_('expression PLUSOP expression')
    def expression(self, p):
        """Implement the <expression> production alternate for <expression> + <expression>."""
        return BinOp("PLUSOP", p.expression0, p.expression1)

    @_('expression MINUSOP expression')
    def expression(self, p):
        """Implement the <expression> production alternate for <expression> - <expression>."""
        return BinOp("MINUSOP", p.expression0, p.expression1)

    # <term> ::= <term> <multop> <factor> | <factor>
    # <multop> ::= * | /

    @_('expression MULTIPLYOP expression')
    def expression(self, p):
        """Implement the <expression> production alternate for <expression> * <expression>.

        Because precedence for the operators is defined, we don't need
        a separate <term> rule.
        """
        return BinOp("MULTIPLYOP", p.expression0, p.expression1)

    @_('expression DIVIDEOP expression')
    def expression(self, p):
        """Implement the <expression> production alternate for <expression> / <expression>.

        Because precedence for the operators is defined, we don't need
        a separate <term> rule.
        """
        return BinOp("DIVIDEOP", p.expression0, p.expression1)


    # <factor> ::= <constant> | <identifier>
    #            | <identifier> [ <expression>]
    #            | ( <expression> ) | <identifier> ( <arguments> )
    #            | <identifier> ( )


    @_('constant')
    def expression(self, p):
        """Implement the <expression> production alternate for integer constants.

        Because precedence for the operators is defined, we don't need
        a separate <factor> rule.
        """
        return p.constant

    @_('INTCONSTANT')
    def constant(self, p):
        """Implement the <constant> production for integer constants."""
        return Integer(int(p.INTCONSTANT))

    @_('variable')
    def expression(self, p):
        """Implement the <expression> production alternate for variable identifiers.

        Because precedence for the operators is defined, we don't need
        a separate <factor> rule.
        """
        return p.variable

    @_('IDENTIFIER')
    def variable(self, p):
        """Implement a <variable> production, because we keep reusing it."""
        return Variable(p.IDENTIFIER)

    @_('variable OPENSQUARE expression CLOSESQUARE')
    def expression(self, p):
        """Implement the <expression> production alternate for array element read."""
        return ArrayIndex(p.variable, p.expression)

    @_('OPENPAREN expression CLOSEPAREN')
    def expression(self, p):
        """Implement the <expression> production alternate for (<expression>).

        Because precedence for the operators is defined, we don't need
        a separate <factor> rule.
        """
        return p.expression

    @_('IDENTIFIER OPENPAREN arguments CLOSEPAREN')
    def expression(self, p):
        """Implement the <expression> production alternate for a function call with arguments."""
        return FunctionCall(p.IDENTIFIER, p.arguments)

    @_('IDENTIFIER OPENPAREN CLOSEPAREN')
    def expression(self, p):
        """Implement the <expression> production alternate for a function call without arguments."""
        return FunctionCall(p.IDENTIFIER)


    # <bexpression> ::= <expression> <relop> <expression>
    # <relop> ::= < | <= | == | >= | > | !=

    @_('expression LEOP expression')
    def bexpression(self, p):
        """Implement the <bexpression> alternate for <expression> <= <expression>."""
        return RelOp("LEOP", p.expression0, p.expression1)

    @_('expression LTOP expression')
    def bexpression(self, p):
        """Implement the <bexpression> alternate for <expression> < <expression>."""
        return RelOp("LTOP", p.expression0, p.expression1)

    @_('expression GEOP expression')
    def bexpression(self, p):
        """Implement the <bexpression> alternate for <expression> >= <expression>."""
        return RelOp("GEOP", p.expression0, p.expression1)

    @_('expression GTOP expression')
    def bexpression(self, p):
        """Implement the <bexpression> alternate for <expression> < <expression>."""
        return RelOp("GTOP", p.expression0, p.expression1)

    @_('expression EQOP expression')
    def bexpression(self, p):
        """Implement the <bexpression> alternate for <expression> == <expression>."""
        return RelOp("EQOP", p.expression0, p.expression1)

    @_('expression NEOP expression')
    def bexpression(self, p):
        """Implement the <bexpression> alternate for <expression> != <expression>."""
        return RelOp("NEOP", p.expression0, p.expression1)

    # <arguments> ::= <expression> | <expression> , <arguments>

    @_('expression')
    def arguments(self, p):
        """Implement the <arguments> production alternate for a single argument."""
        return Arguments(p.expression)

    @_('expression COMMA arguments')
    def arguments(self, p):
        """Implement the <arguments> production alternate for a sequence of arguments."""
        node = p.arguments

        if p.expression:
            node.prepend(p.expression)

        return node



    # <empty> has the obvious meaning

    @_('')
    def empty(self, p):
        """Implement the <empty> production."""
        pass

