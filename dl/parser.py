# -----------------------------------------------------------------------------
# parser.py
# -----------------------------------------------------------------------------

import sys
sys.path.append('.')

from sly import Parser
from dl.lexer import DLLexer
from dl.ast import Integer, Variable, BinOp, RelOp, Print, While, Block, Program

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
        """Implement the <program> production."""
        return Program(p.block)

    # <declarations> ::= <declaration>
    #                  | <declaration> <declarations>
    # <declaration> ::= <variabledeclaration> | <functiondeclaration>
    # <variabledeclaration> ::= int <vardeflist> ;
    # <vardeflist> ::= <vardec> | <vardec> , <vardeflist>
    # <vardec> ::= <identifier> | <identifier> [ <constant> ]
    # <functiondeclaration> ::= <identifier> (); <functionbody>
    #                         | <identifier> ( <arglist> ); <functionbody>
    # <functionbody> ::= <variabledeclaration> <block> | <block>
    # <arglist> ::= <identifier> | <identifier> , <arglist>

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

    @_('printstatement')
    def statement(self, p):
        """Implement the <statement> production alternate for <printstatement>."""
        return p.printstatement

    @_('empty')
    def statement(self, p):
        """Implement the <statement> production alternate for <empty>."""
        pass

    # <assignment> ::= <identifier> = <expression>
    #                | <identifier> [ <expression> ] = <expression>
    # <ifstatement> ::= if ( <bexpression> ) <block> else <block>
    #                 | if ( <bexpression> ) <block>
    # <whilestatement> ::= while ( <bexpression> ) <block>


    # <printstatement> ::= print ( <expression> )

    @_('PRINT OPENPAREN expression CLOSEPAREN')
    def printstatement(self, p):
        """Implement the <printstatement> production."""
        return Print(p.expression)

    # <readstatement> ::= read ( <identifier> )
    # <returnstatement> ::= return <expression>
    # <expression> ::= <expression> <addingop> <term>
    #                | <term> | <addingop> <term>
    # <addingop> ::= + | -

    @_('expression PLUSOP expression')
    def expression(self, p):
        """Implement the <expression> alternate for <expression> + <expression>."""
        return BinOp("PLUSOP", p.expression0, p.expression1)

    # <term> ::= <term> <multop> <factor> | <factor>
    # <multop> ::= * | /
    # <factor> ::= <constant> | <identifier>
    #            | <identifier> [ <expression>]
    #            | ( <expression> ) | <identifier> ( <arguments> )
    #            | <identifier> ( )


    @_('INTCONSTANT')
    def expression(self, p):
        """Implement the <expression> alternate for integer constants.

        Because precedence for the operators is defined, we don't need
        a separate <factor> rule.
        """
        return Integer(int(p.INTCONSTANT))

    @_('IDENTIFIER')
    def expression(self, p):
        """Implement the <expression> alternate for variable identifiers.

        Because precedence for the operators is defined, we don't need
        a separate <factor> rule.
        """
        return Variable(p.IDENTIFIER)

    # <bexpression> ::= <expression> <relop> <expression>
    # <relop> ::= < | <= | == | >= | > | !=

    @_('expression LEOP expression')
    def bexpression(self, p):
        """Implement the <bexpression> alternate for <expression> <= <expression>."""
        return RelOp("LEOP", p.expression0, p.expression1)

    # <arguments> ::= <expression> | <expression> , <arguments>


    # <empty> has the obvious meaning

    @_('')
    def empty(self, p):
        """Implement the <empty> production."""
        pass

