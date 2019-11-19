#!/usr/bin/env python3

import sys
sys.path.append('.')

from dl.lexer import DLLexer
from dl.parser import DLParser
from dl.semantic import DLSemanticAnalyzer, SemanticError

if __name__ == '__main__':
    lexer = DLLexer()
    parser = DLParser()
    analyzer = DLSemanticAnalyzer()
    while True:
        try:
            text = input('dl > ')
        except EOFError:
            print("\n")
            break
        if text:
            ast = parser.parse(lexer.tokenize(text))
            if ast:
                try:
                    result = analyzer.analyze(ast)
                except SemanticError as err:
                    print(err.message)
                else:
                    print(result)
