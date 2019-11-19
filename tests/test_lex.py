import unittest

import sys
sys.path.append('.')


from dl.lexer import DLLexer

class TestLexer(unittest.TestCase):

    def test_tokens_single_operator(self):
        lexer = DLLexer()
        tokens = list(lexer.tokenize('; , + - / * ( ) { } [ ]'))

        self.assertEqual(tokens[0].value, ';')
        self.assertEqual(tokens[0].type, 'SEMICOLON')

        self.assertEqual(tokens[1].value, ',')
        self.assertEqual(tokens[1].type, 'COMMA')

        self.assertEqual(tokens[2].value, '+')
        self.assertEqual(tokens[2].type, 'PLUSOP')

        self.assertEqual(tokens[3].value, '-')
        self.assertEqual(tokens[3].type, 'MINUSOP')

        self.assertEqual(tokens[4].value, '/')
        self.assertEqual(tokens[4].type, 'DIVIDEOP')

        self.assertEqual(tokens[5].value, '*')
        self.assertEqual(tokens[5].type, 'MULTIPLYOP')

        self.assertEqual(tokens[6].value, '(')
        self.assertEqual(tokens[6].type, 'OPENPAREN')

        self.assertEqual(tokens[7].value, ')')
        self.assertEqual(tokens[7].type, 'CLOSEPAREN')

        self.assertEqual(tokens[8].value, '{')
        self.assertEqual(tokens[8].type, 'OPENCURLY')

        self.assertEqual(tokens[9].value, '}')
        self.assertEqual(tokens[9].type, 'CLOSECURLY')

        self.assertEqual(tokens[10].value, '[')
        self.assertEqual(tokens[10].type, 'OPENSQUARE')

        self.assertEqual(tokens[11].value, ']')
        self.assertEqual(tokens[11].type, 'CLOSESQUARE')


    def test_tokens_lookahead_operator(self):
        lexer = DLLexer()
        tokens = list(lexer.tokenize('= < <= > >= == !='))

        self.assertEqual(tokens[0].value, '=')
        self.assertEqual(tokens[0].type, 'ASSIGNOP')

        self.assertEqual(tokens[1].value, '<')
        self.assertEqual(tokens[1].type, 'LTOP')

        self.assertEqual(tokens[2].value, '<=')
        self.assertEqual(tokens[2].type, 'LEOP')

        self.assertEqual(tokens[3].value, '>')
        self.assertEqual(tokens[3].type, 'GTOP')

        self.assertEqual(tokens[4].value, '>=')
        self.assertEqual(tokens[4].type, 'GEOP')

        self.assertEqual(tokens[5].value, '==')
        self.assertEqual(tokens[5].type, 'EQOP')

        self.assertEqual(tokens[6].value, '!=')
        self.assertEqual(tokens[6].type, 'NEOP')


    def test_tokens_constants(self):
        lexer = DLLexer()
        tokens = list(lexer.tokenize('123'))

        self.assertEqual(tokens[0].value, '123')
        self.assertEqual(tokens[0].type, 'INTCONSTANT')


    def test_tokens_identifiers(self):
        lexer = DLLexer()
        tokens = list(lexer.tokenize('abc d123 e1c2'))

        self.assertEqual(tokens[0].value, 'abc')
        self.assertEqual(tokens[0].type, 'IDENTIFIER')

        self.assertEqual(tokens[1].value, 'd123')
        self.assertEqual(tokens[1].type, 'IDENTIFIER')

        self.assertEqual(tokens[2].value, 'e1c2')
        self.assertEqual(tokens[2].type, 'IDENTIFIER')


    def test_tokens_keywords(self):
        lexer = DLLexer()
        tokens = list(lexer.tokenize('else if int print read return while'))

        self.assertEqual(tokens[0].value, 'else')
        self.assertEqual(tokens[0].type, 'ELSE')

        self.assertEqual(tokens[1].value, 'if')
        self.assertEqual(tokens[1].type, 'IF')

        self.assertEqual(tokens[2].value, 'int')
        self.assertEqual(tokens[2].type, 'INT')

        self.assertEqual(tokens[3].value, 'print')
        self.assertEqual(tokens[3].type, 'PRINT')

        self.assertEqual(tokens[4].value, 'read')
        self.assertEqual(tokens[4].type, 'READ')

        self.assertEqual(tokens[5].value, 'return')
        self.assertEqual(tokens[5].type, 'RETURN')

        self.assertEqual(tokens[6].value, 'while')
        self.assertEqual(tokens[6].type, 'WHILE')

    def test_tokens_comments(self):
        lexer = DLLexer()
        tokens = list(lexer.tokenize('/* ignore comment */ foo'))

        self.assertEqual(tokens[0].value, 'foo')
        self.assertEqual(tokens[0].type, 'IDENTIFIER')


    def test_tokens_code_example(self):
        lexer = DLLexer()

        source_file = open("tests/simple.dl",'r')
        source_string = source_file.read()

        tokens = list(lexer.tokenize(source_string))
        source_file.close()

        self.assertEqual(lexer.lineno, 17)

        self.assertEqual(tokens[0].value, 'factorial')
        self.assertEqual(tokens[0].type, 'IDENTIFIER')

        self.assertEqual(tokens[1].value, '(')
        self.assertEqual(tokens[1].type, 'OPENPAREN')

        self.assertEqual(tokens[2].value, 'n')
        self.assertEqual(tokens[2].type, 'IDENTIFIER')

        self.assertEqual(tokens[3].value, ')')
        self.assertEqual(tokens[3].type, 'CLOSEPAREN')

        self.assertEqual(tokens[4].value, ';')
        self.assertEqual(tokens[4].type, 'SEMICOLON')

        self.assertEqual(tokens[5].value, '{')
        self.assertEqual(tokens[5].type, 'OPENCURLY')

        self.assertEqual(tokens[6].value, 'if')
        self.assertEqual(tokens[6].type, 'IF')

        self.assertEqual(tokens[8].value, 'n')
        self.assertEqual(tokens[8].type, 'IDENTIFIER')

        self.assertEqual(tokens[9].value, '==')
        self.assertEqual(tokens[9].type, 'EQOP')

        self.assertEqual(tokens[10].value, '0')
        self.assertEqual(tokens[10].type, 'INTCONSTANT')

        self.assertEqual(tokens[13].value, 'return')
        self.assertEqual(tokens[13].type, 'RETURN')

        self.assertEqual(tokens[14].value, '1')
        self.assertEqual(tokens[14].type, 'INTCONSTANT')

        self.assertEqual(tokens[16].value, 'else')
        self.assertEqual(tokens[16].type, 'ELSE')

        self.assertEqual(tokens[20].value, '*')
        self.assertEqual(tokens[20].type, 'MULTIPLYOP')

        self.assertEqual(tokens[24].value, '-')
        self.assertEqual(tokens[24].type, 'MINUSOP')

        self.assertEqual(tokens[28].value, '}')
        self.assertEqual(tokens[28].type, 'CLOSECURLY')

        self.assertEqual(tokens[29].value, 'int')
        self.assertEqual(tokens[29].type, 'INT')

        self.assertEqual(tokens[30].value, 'x')
        self.assertEqual(tokens[30].type, 'IDENTIFIER')

        self.assertEqual(tokens[34].value, '=')
        self.assertEqual(tokens[34].type, 'ASSIGNOP')

        self.assertEqual(tokens[37].value, 'while')
        self.assertEqual(tokens[37].type, 'WHILE')

        self.assertEqual(tokens[40].value, '<=')
        self.assertEqual(tokens[40].type, 'LEOP')

        self.assertEqual(tokens[41].value, '10')
        self.assertEqual(tokens[41].type, 'INTCONSTANT')

        self.assertEqual(tokens[44].value, 'print')
        self.assertEqual(tokens[44].type, 'PRINT')

        self.assertEqual(tokens[55].value, '+')
        self.assertEqual(tokens[55].type, 'PLUSOP')

        self.assertEqual(tokens[58].value, '}')
        self.assertEqual(tokens[58].type, 'CLOSECURLY')



if __name__ == '__main__':
    unittest.main()
