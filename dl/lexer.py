# -----------------------------------------------------------------------------
# lexer.py
# -----------------------------------------------------------------------------

import sys
sys.path.append('.')

from sly import Lexer

class DLLexer(Lexer):
    tokens = { ELSE, IF, INT, PRINT, READ, RETURN, WHILE,
               SEMICOLON, COMMA, OPENCURLY, CLOSECURLY,
               OPENSQUARE, CLOSESQUARE, OPENPAREN, CLOSEPAREN,
               DIVIDEOP, MULTIPLYOP, PLUSOP, MINUSOP, ASSIGNOP,
               EQOP, NEOP, LTOP, LEOP, GTOP, GEOP,
               INTCONSTANT, IDENTIFIER }

    # Ignored whitespace characters
    ignore = ' \t'
    ignore_newline = r'\n+'

    # Ignored comments
    ignore_comment = r'/\*[^*]+\*/'


    # Tokens
    IDENTIFIER = r'[a-z][a-z0-9]*'
    IDENTIFIER['else'] = ELSE
    IDENTIFIER['if'] = IF
    IDENTIFIER['int'] = INT
    IDENTIFIER['print'] = PRINT
    IDENTIFIER['read'] = READ
    IDENTIFIER['return'] = RETURN
    IDENTIFIER['while'] = WHILE

    INTCONSTANT = r'\d+'

    # Special symbols
    SEMICOLON = r';'
    COMMA = r','
    PLUSOP = r'\+'
    MINUSOP = r'-'
    DIVIDEOP = r'/'
    MULTIPLYOP = r'\*'
    OPENPAREN = r'\('
    CLOSEPAREN = r'\)'
    OPENCURLY = r'\{'
    CLOSECURLY = r'\}'
    OPENSQUARE = r'\['
    CLOSESQUARE = r'\]'
    LEOP = r'<='
    LTOP = r'<'
    GEOP = r'>='
    GTOP = r'>'
    EQOP = r'=='
    ASSIGNOP = r'='
    NEOP = r'!='


    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
