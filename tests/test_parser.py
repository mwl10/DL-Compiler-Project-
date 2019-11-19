import unittest

import sys
sys.path.append('.')


from dl.lexer import DLLexer
from dl.parser import DLParser
from dl.ast import Integer, Variable, BinOp, RelOp, ArrayIndex, \
                   Assign, Print, Read, Return, If, While, Block, \
                   FunctionCall, Arguments, FunctionDeclaration, \
                   Declarations, VariableDeclarations, Program

class TestParser(unittest.TestCase):

    def test_parse_print_statement(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ print(1) }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Print(Integer(1))))")

    def test_parse_addition_constants(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ print(2 + 3) }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Print(BinOp(PLUSOP, Integer(2), Integer(3)))))")

    def test_parse_addition_variables(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ print(x + y) }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Print(BinOp(PLUSOP, Variable(x), Variable(y)))))")

    @unittest.skip("Assignment statements not implemented yet")
    def test_parse_assignment_statement(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ x = 5 }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Assign(Variable(x), Integer(5))))")

    @unittest.skip("Assignment statements not implemented yet")
    def test_parse_addition_assignment(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ x = 2 + 3 }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Assign(Variable(x), BinOp(PLUSOP, Integer(2), Integer(3)))))")

    @unittest.skip("Assignment statements not implemented yet")
    def test_parse_subtraction_assignment(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ x = 4 - 3 }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Assign(Variable(x), BinOp(MINUSOP, Integer(4), Integer(3)))))")

    @unittest.skip("Assignment statements not implemented yet")
    def test_parse_multiplication_assignment(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ x = 4 * 5 }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Assign(Variable(x), BinOp(MULTIPLYOP, Integer(4), Integer(5)))))")

    @unittest.skip("Assignment statements not implemented yet")
    def test_parse_division_assignment(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ x = 10 / 2 }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Assign(Variable(x), BinOp(DIVIDEOP, Integer(10), Integer(2)))))")

    @unittest.skip("Assignment to array elements not implemented yet")
    def test_parse_assignment_statement_to_array_constant(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ x[1] = 5 }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Assign(ArrayIndex(Variable(x), Integer(1)), Integer(5))))")

    @unittest.skip("Assignment to array elements not implemented yet")
    def test_parse_assignment_statement_to_array_variable(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ x[y] = z }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Assign(ArrayIndex(Variable(x), Variable(y)), Variable(z))))")

    @unittest.skip("Assignment from array elements not implemented yet")
    def test_parse_assignment_statement_from_array_constant(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ x = y[1] }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Assign(Variable(x), ArrayIndex(Variable(y), Integer(1)))))")

    @unittest.skip("Assignment from array elements not implemented yet")
    def test_parse_assignment_statement_from_array_variable(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ x = y[z] }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Assign(Variable(x), ArrayIndex(Variable(y), Variable(z)))))")

    @unittest.skip("Read statement not implemented yet")
    def test_parse_read_statement(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ read(x) }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Read(Variable(x))))")

    @unittest.skip("Return statement not implemented yet")
    def test_parse_return_statement_constant(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ return(2) }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Return(Integer(2))))")

    @unittest.skip("Return statement not implemented yet")
    def test_parse_return_statement_variable(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ return(x) }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Return(Variable(x))))")

    @unittest.skip("Return statement not implemented yet")
    def test_parse_return_statement_expression(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ return(x + 5) }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Return(BinOp(PLUSOP, Variable(x), Integer(5)))))")

    @unittest.skip("If statement not implemented yet")
    def test_parse_if_statement(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ if(1 == 1) {print(1)} }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(If(RelOp(EQOP, Integer(1), Integer(1)), Block(Print(Integer(1))))))")

    @unittest.skip("If statement not implemented yet")
    def test_parse_if_else_statement(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ if(1 == 5) {print(1)} else {print(0)} }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(If(RelOp(EQOP, Integer(1), Integer(5)), Block(Print(Integer(1))), Block(Print(Integer(0))))))")

    @unittest.skip("While statement not implemented yet")
    def test_parse_while_statement(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ while(1 == 1) {print(1)} }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(While(RelOp(EQOP, Integer(1), Integer(1)), Block(Print(Integer(1))))))")

    @unittest.skip("While statement not implemented yet")
    def test_parse_not_equal_relop(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ while(1 != 2) {print(2)} }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(While(RelOp(NEOP, Integer(1), Integer(2)), Block(Print(Integer(2))))))")

    @unittest.skip("While statement not implemented yet")
    def test_parse_less_than_relop(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ while(2 < 3) {print(3)} }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(While(RelOp(LTOP, Integer(2), Integer(3)), Block(Print(Integer(3))))))")

    @unittest.skip("While statement not implemented yet")
    def test_parse_less_or_equal_relop(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ while(3 <= 4) {print(4)} }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(While(RelOp(LEOP, Integer(3), Integer(4)), Block(Print(Integer(4))))))")

    @unittest.skip("While statement not implemented yet")
    def test_parse_greater_than_relop(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ while(5 > 4) {print(5)} }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(While(RelOp(GTOP, Integer(5), Integer(4)), Block(Print(Integer(5))))))")

    @unittest.skip("While statement not implemented yet")
    def test_parse_greater_or_equal_relop(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ while(6 >= 5) {print(6)} }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(While(RelOp(GEOP, Integer(6), Integer(5)), Block(Print(Integer(6))))))")

    @unittest.skip("Block as a statement not implemented yet")
    def test_parse_block_statement(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ {print(1)} }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Block(Print(Integer(1)))))")

    @unittest.skip("Statement sequences not implemented yet")
    def test_parse_statement_sequence(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ x = 2; print(x) }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Assign(Variable(x), Integer(2)), Print(Variable(x))))")

    @unittest.skip("Variable declarations not implemented yet")
    def test_parse_program_variable_declaration(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = """
            int x;
            {
                x = 1
            }
        """
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Declarations(VariableDeclarations(INT, Variable(x))), Block(Assign(Variable(x), Integer(1))))")

    @unittest.skip("Variable declaration sequences not implemented yet")
    def test_parse_program_variable_declaration_sequence(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = """
            int x, y, z;
            {
                x = 1
            }
        """
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Declarations(VariableDeclarations(INT, Variable(x), Variable(y), Variable(z))), Block(Assign(Variable(x), Integer(1))))")

    @unittest.skip("Array declarations not implemented yet")
    def test_parse_program_array_declaration(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = """
            int x[10];
            {
                x[5] = 1
            }
        """
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Declarations(VariableDeclarations(INT, ArrayIndex(Variable(x), Integer(10)))), Block(Assign(ArrayIndex(Variable(x), Integer(5)), Integer(1))))")


    @unittest.skip("Function calls not implemented yet")
    def test_parse_function_call_constant(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ x = foo(1) }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Assign(Variable(x), FunctionCall(foo, Arguments(Integer(1))))))")

    @unittest.skip("Function calls not implemented yet")
    def test_parse_function_call_variable(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ x = bar(y) }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Assign(Variable(x), FunctionCall(bar, Arguments(Variable(y))))))")

    @unittest.skip("Function calls not implemented yet")
    def test_parse_function_call_multiple_arguments(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = "{ x = baz(y, 1, z, 2) }"
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Block(Assign(Variable(x), FunctionCall(baz, Arguments(Variable(y), Integer(1), Variable(z), Integer(2))))))")

    @unittest.skip("Function declarations not implemented yet")
    def test_parse_function_declaration_no_arguments(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = """
            /* Declare a function named 'foo', with no arguments. */
            foo(); { return(5); }

            /* Call 'foo' in the main body of the program. */
            {
                x = foo()
            }
        """
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertEqual(str(result), "Program(Declarations(FunctionDeclaration(foo, Block(Return(Integer(5))))), Block(Assign(Variable(x), FunctionCall(foo))))")

    @unittest.skip("Function declarations not implemented yet")
    def test_parse_function_declaration_one_argument(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = """
            /* Declare a function named 'bar', with one argument. */
            bar(x); { return(x * 10); }

            /* Call 'bar' in the main body of the program. */
            {
                y = bar(5)
            }
        """
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertIsInstance(result, Program)
        self.assertEqual(str(result.declarations), "Declarations(FunctionDeclaration(bar, Arguments(Variable(x)), Block(Return(BinOp(MULTIPLYOP, Variable(x), Integer(10))))))")
        self.assertEqual(str(result.body), "Block(Assign(Variable(y), FunctionCall(bar, Arguments(Integer(5)))))")


    @unittest.skip("Function declarations not implemented yet")
    def test_parse_function_declaration_with_variables(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = """
            /* Declare a function named 'baz', with a variable declaration. */
            baz();
            int x;
            {
                return(x + 2)
            }

            /* Call 'baz' in the main body of the program. */
            {
                y = baz(3)
            }
        """
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertIsInstance(result, Program)
        self.assertEqual(str(result.body), "Block(Assign(Variable(y), FunctionCall(baz, Arguments(Integer(3)))))")

        decs = result.declarations
        self.assertIsInstance(decs, Declarations)
        func = decs.declarations[0]
        self.assertIsInstance(func, FunctionDeclaration)
        self.assertEqual(func.name, "baz")
        self.assertEqual(func.args, None)
        self.assertEqual(str(func.vars), "VariableDeclarations(INT, Variable(x))")
        self.assertEqual(str(func.body), "Block(Return(BinOp(PLUSOP, Variable(x), Integer(2))))")


    @unittest.skip("Function declarations not implemented yet")
    def test_parse_function_declaration_with_arguments_and_variables(self):
        lexer = DLLexer()
        parser = DLParser()

        source_string = """
            /* Declare a function named 'buz', with one argument, and a variable declaration. */
            buz(x);
            int y;
            {
                y = 2;
                return(x * y)
            }

            /* Call 'buz' in the main body of the program. */
            {
                z = buz(3)
            }
        """
        tokens = lexer.tokenize(source_string)
        result = parser.parse(tokens)

        self.assertIsInstance(result, Program)
        self.assertEqual(str(result.declarations), "Declarations(FunctionDeclaration(buz, Arguments(Variable(x)), VariableDeclarations(INT, Variable(y)), Block(Assign(Variable(y), Integer(2)), Return(BinOp(MULTIPLYOP, Variable(x), Variable(y))))))")
        self.assertEqual(str(result.body), "Block(Assign(Variable(z), FunctionCall(buz, Arguments(Integer(3)))))")


    @unittest.skip("Necessary productions not implemented yet")
    def test_parse_code_example(self):
        lexer = DLLexer()
        parser = DLParser()

        source_file = open("tests/simple.dl",'r')
        source_string = source_file.read()

        tokens = lexer.tokenize(source_string)
        source_file.close()

        result = parser.parse(tokens)

        self.assertIsInstance(result, Program)

        decs = result.declarations
        self.assertIsInstance(decs, Declarations)
        func = decs.declarations[0]
        self.assertIsInstance(func, FunctionDeclaration)
        self.assertEqual(func.name, "factorial")
        self.assertEqual(str(func.args), "Arguments(Variable(n))")
        self.assertEqual(func.vars, None)
        self.assertIsInstance(func.body, Block)

        conditional = func.body.statements[0]
        self.assertIsInstance(conditional, If)
        self.assertEqual(str(conditional.condition), "RelOp(EQOP, Variable(n), Integer(0))")
        self.assertEqual(str(conditional.body_true), "Block(Return(Integer(1)))")
        self.assertEqual(str(conditional.body_else), "Block(Return(BinOp(MULTIPLYOP, Variable(n), FunctionCall(factorial, Arguments(BinOp(MINUSOP, Variable(n), Integer(1)))))))")


        main_vars = decs.declarations[1]
        self.assertIsInstance(main_vars, VariableDeclarations)
        self.assertEqual(str(main_vars), "VariableDeclarations(INT, Variable(x))")

        main = result.body
        self.assertIsInstance(main, Block)
        first = main.statements[0]
        self.assertEqual(str(first), "Assign(Variable(x), Integer(1))")
        second = main.statements[1]
        self.assertIsInstance(second, While)
        self.assertEqual(str(second.condition), "RelOp(LEOP, Variable(x), Integer(10))")
        self.assertEqual(str(second.body), "Block(Print(FunctionCall(factorial, Arguments(Variable(x)))), Assign(Variable(x), BinOp(PLUSOP, Variable(x), Integer(1))))")


if __name__ == '__main__':
    unittest.main()
