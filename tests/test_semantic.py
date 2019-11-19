import unittest

import os
import sys
sys.path.append('.')


from dl.lexer import DLLexer
from dl.parser import DLParser
from dl.semantic import DLSemanticAnalyzer, UndeclaredVariableError, UndeclaredFunctionError, TypeCheckError

class TestGenerator(unittest.TestCase):

    def test_semantic_print_constant(self):
        ast = self.build_ast("{ print(1) }")
        analyzer = DLSemanticAnalyzer()
        result = analyzer.analyze(ast)
        self.assertEqual(str(result), "Program(Block(Print(Integer(1))))")

        # Test inferred type of integer constant
        main_body = result.body
        print_statement = main_body.statements[0]
        self.assertEqual(print_statement.arg.itype, "int")


    @unittest.skip("Semantic check for undeclared variables not implemented yet")
    def test_semantic_undeclared_variable_print(self):
        with self.assertRaises(UndeclaredVariableError):
            ast = self.build_ast("{ print(a) }")
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)


    def test_semantic_declared_variable_print(self):
        source_string = """
            int b;
            {
                print(b)
            }
        """
        ast = self.build_ast(source_string)
        analyzer = DLSemanticAnalyzer()
        result = analyzer.analyze(ast)
        self.assertEqual(str(result), "Program(Declarations(VariableDeclarations(INT, Variable(b))), Block(Print(Variable(b))))")

        # Test inferred type of variable
        main_body = result.body
        print_statement = main_body.statements[0]
        # self.assertEqual(print_statement.arg.itype, "int")


    def test_semantic_addition_constants(self):
        source_string = "{ print(2 + 3) }"
        ast = self.build_ast(source_string)
        analyzer = DLSemanticAnalyzer()
        result = analyzer.analyze(ast)
        self.assertEqual(str(result), "Program(Block(Print(BinOp(PLUSOP, Integer(2), Integer(3)))))")

        # Test inferred type of addition operation
        main_body = result.body
        print_statement = main_body.statements[0]
        # self.assertEqual(print_statement.arg.itype, "int")

    @unittest.skip("Semantic check for undeclared variables not implemented yet")
    def test_semantic_undeclared_variable_addition(self):
        with self.assertRaises(UndeclaredVariableError):
            ast = self.build_ast("{ print(c + 1) }")
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)

    def test_semandic_declared_variable_addition(self):
        source_string = """
            int d;
            {
                print(d + 5)
            }
        """
        ast = self.build_ast(source_string)
        analyzer = DLSemanticAnalyzer()
        result = analyzer.analyze(ast)
        lexer = DLLexer()
        parser = DLParser()

        self.assertEqual(str(result), "Program(Declarations(VariableDeclarations(INT, Variable(d))), Block(Print(BinOp(PLUSOP, Variable(d), Integer(5)))))")

        # Test inferred type of addition operation
        main_body = result.body
        print_statement = main_body.statements[0]
        # self.assertEqual(print_statement.arg.itype, "int")


    @unittest.skip("Semantic check for undeclared variables not implemented yet")
    def test_semantic_undeclared_variable_assign(self):
        with self.assertRaises(UndeclaredVariableError):
            ast = self.build_ast("{ e = 1 }")
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)


    @unittest.skip("Inferred type for variables not implemented yet")
    def test_semantic_declared_variable_assign(self):
        source_string = """
            int f;
            {
                f = 1
            }
        """
        ast = self.build_ast(source_string)
        analyzer = DLSemanticAnalyzer()
        result = analyzer.analyze(ast)
        self.assertEqual(str(result), "Program(Declarations(VariableDeclarations(INT, Variable(f))), Block(Assign(Variable(f), Integer(1))))")

        # Test inferred type of assignment statement
        main_body = result.body
        assign_statement = main_body.statements[0]
        self.assertEqual(assign_statement.itype, "int")

    @unittest.skip("Semantic check for undeclared arrays not implemented yet")
    def test_semantic_undeclared_array_assign(self):
        with self.assertRaises(UndeclaredVariableError):
            ast = self.build_ast("{ g[1] = 5 }")
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)

    @unittest.skip("Inferred type for array index assignment not implemented yet")
    def test_semantic_declared_array_assign(self):
        source_string = """
            int h[10];
            {
                h[1] = 5
            }
        """
        ast = self.build_ast(source_string)
        analyzer = DLSemanticAnalyzer()
        result = analyzer.analyze(ast)
        self.assertEqual(str(result), "Program(Declarations(VariableDeclarations(INT, ArrayIndex(Variable(h), Integer(10)))), Block(Assign(ArrayIndex(Variable(h), Integer(1)), Integer(5))))")

        # Test inferred type of array index
        main_body = result.body
        assign_statement = main_body.statements[0]
        self.assertEqual(assign_statement.left.itype, "int")
 
    @unittest.skip("Semantic check for undeclared arrays not implemented yet")
    def test_semantic_undeclared_array_assign_from(self):
        with self.assertRaises(UndeclaredVariableError):
            source_string = """
                int i;
                {
                    i = j[1] 
                }
            """
            ast = self.build_ast(source_string)
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)

    @unittest.skip("Inferred type for array index access not implemented yet")
    def test_semantic_declared_array_assign_from(self):
        source_string = """
            int k, l[20];
            {
                k = l[1] 
            }
        """
        ast = self.build_ast(source_string)
        analyzer = DLSemanticAnalyzer()
        result = analyzer.analyze(ast)
        self.assertEqual(str(result), "Program(Declarations(VariableDeclarations(INT, Variable(k), ArrayIndex(Variable(l), Integer(20)))), Block(Assign(Variable(k), ArrayIndex(Variable(l), Integer(1)))))")

        # Test inferred type of array index
        main_body = result.body
        assign_statement = main_body.statements[0]
        self.assertEqual(assign_statement.right.itype, "int")

    @unittest.skip("Semantic check for undeclared variables not implemented yet")
    def test_semantic_undeclared_variable_read(self):
        with self.assertRaises(UndeclaredVariableError):
            ast = self.build_ast("{ read(m) }")
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)

    def test_semantic_declared_variable_read(self):
        source_string = """
            int n;
            {
                read(n) 
            }
        """
        ast = self.build_ast(source_string)
        analyzer = DLSemanticAnalyzer()
        result = analyzer.analyze(ast)
        self.assertEqual(str(result), "Program(Declarations(VariableDeclarations(INT, Variable(n))), Block(Read(Variable(n))))")

        # Test inferred type of argument to read statement
        main_body = result.body
        read_statement = main_body.statements[0]
        # self.assertEqual(read_statement.result.itype, "int")

    @unittest.skip("Semantic check for undeclared variables not implemented yet")
    def test_semantic_undeclared_variable_return(self):
        with self.assertRaises(UndeclaredVariableError):
            ast = self.build_ast("{ return o }")
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)

    def test_semantic_declared_variable_return(self):
        source_string = """
            int p;
            {
                return p
            }
        """
        ast = self.build_ast(source_string)
        analyzer = DLSemanticAnalyzer()
        result = analyzer.analyze(ast)
        self.assertEqual(str(result), "Program(Declarations(VariableDeclarations(INT, Variable(p))), Block(Return(Variable(p))))")

        # Test inferred type of argument to return statement
        main_body = result.body
        return_statement = main_body.statements[0]
        # self.assertEqual(return_statement.result.itype, "int")

    @unittest.skip("Semantic check for undeclared variables not implemented yet")
    def test_semantic_undeclared_variable_if_condition(self):
        with self.assertRaises(UndeclaredVariableError):
            source_string = """
                int r;
                {
                    if(q == 1) { print(r) }
                }
            """
            ast = self.build_ast(source_string)
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)

    @unittest.skip("Semantic check for undeclared variables not implemented yet")
    def test_semantic_undeclared_variable_if_true_block(self):
        with self.assertRaises(UndeclaredVariableError):
            source_string = """
                int q;
                {
                    if(q == 1) { print(r) }
                }
            """
            ast = self.build_ast(source_string)
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)

    @unittest.skip("Semantic check for undeclared variables not implemented yet")
    def test_semantic_undeclared_variable_if_false_block(self):
        with self.assertRaises(UndeclaredVariableError):
            source_string = """
                int q, r;
                {
                    if (q == 1) { print(r) }
                    else { print(s) }
                }
            """
            ast = self.build_ast(source_string)
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)

    @unittest.skip("Inferred type for variables not implemented yet")
    def test_semantic_declared_variable_if(self):
        source_string = """
            int q, r, s;
            {
                if (q == 1) { print(r) }
                else { print(s) }
            }
        """
        ast = self.build_ast(source_string)
        analyzer = DLSemanticAnalyzer()
        result = analyzer.analyze(ast)

        self.assertEqual(str(result.declarations), "Declarations(VariableDeclarations(INT, Variable(q), Variable(r), Variable(s)))")
        main_body = result.body
        if_statement = main_body.statements[0]
        self.assertEqual(str(if_statement.condition), "RelOp(EQOP, Variable(q), Integer(1))")
        self.assertEqual(if_statement.condition.itype, "bool")
        self.assertEqual(str(if_statement.body_true), "Block(Print(Variable(r)))")
        self.assertEqual(str(if_statement.body_else), "Block(Print(Variable(s)))")

    @unittest.skip("Semantic check for undeclared variables not implemented yet")
    def test_semantic_undeclared_variable_while_condition(self):
        with self.assertRaises(UndeclaredVariableError):
            source_string = """
                int u;
                {
                    while (t != 1) { print(u) }
                }
            """
            ast = self.build_ast(source_string)
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)

    @unittest.skip("Semantic check for undeclared variables not implemented yet")
    def test_semantic_undeclared_variable_while_block(self):
        with self.assertRaises(UndeclaredVariableError):
            source_string = """
                int t;
                {
                    while(t != 1) { print(u) }
                }
            """
            ast = self.build_ast(source_string)
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)

    @unittest.skip("Inferred type for variables not implemented yet")
    def test_semantic_declared_variable_while(self):
        source_string = """
            int t, u;
            {
                while(t != 1) { print(u) }
            }
        """
        ast = self.build_ast(source_string)
        analyzer = DLSemanticAnalyzer()
        result = analyzer.analyze(ast)

        self.assertEqual(str(result.declarations), "Declarations(VariableDeclarations(INT, Variable(t), Variable(u)))")
        main_body = result.body
        if_statement = main_body.statements[0]
        self.assertEqual(str(if_statement.condition), "RelOp(NEOP, Variable(t), Integer(1))")
        self.assertEqual(if_statement.condition.itype, "bool")
        self.assertEqual(str(if_statement.body), "Block(Print(Variable(u)))")

    @unittest.skip("Semantic check for undeclared variables not implemented yet")
    def test_semantic_undeclared_variable_statement_sequence(self):
        with self.assertRaises(UndeclaredVariableError):
            source_string = """
                int v;
                {
                    v = 7;
                    print(w)
                }
            """
            ast = self.build_ast(source_string)
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)

    @unittest.skip("Inferred type for variables not implemented yet")
    def test_semantic_declared_variable_statement_sequence(self):
        source_string = """
            int v, w;
            {
                v = 7;
                print(w)
            }
        """
        ast = self.build_ast(source_string)
        analyzer = DLSemanticAnalyzer()
        result = analyzer.analyze(ast)
        self.assertEqual(str(result), "Program(Declarations(VariableDeclarations(INT, Variable(v), Variable(w))), Block(Assign(Variable(v), Integer(7)), Print(Variable(w))))")

        # Test inferred type of variable in second statement
        main_body = result.body
        print_statement = main_body.statements[1]
        self.assertEqual(print_statement.arg.itype, "int")


    @unittest.skip("Semantic check for undeclared variables not implemented yet")
    def test_semantic_undeclared_variable_function_call(self):
        with self.assertRaises(UndeclaredVariableError):
            source_string = """
                /* Declare a function named 'fee'. */
                fee(z); { return z - 5; }

                /* Call 'fee' in the main body of the program. */
                int x;
                {
                    x = fee(y)
                }
            """
            ast = self.build_ast(source_string)
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)


    @unittest.skip("Semantic check for undeclared variables not implemented yet")
    def test_semantic_undeclared_variable_function_body(self):
        with self.assertRaises(UndeclaredVariableError):
            source_string = """
                /* Declare a function named 'fie', with no arguments. */
                fie(); { return x / 5; }

                /* Call 'fie' in the main body of the program. */
                int y;
                {
                    y = fie()
                }
            """
            ast = self.build_ast(source_string)
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)


    @unittest.skip("Semantic check for undeclared functions not implemented yet")
    def test_semantic_undeclared_function(self):
        with self.assertRaises(UndeclaredFunctionError):
            source_string = """
                /* Call undeclared function 'foo' in the main body of the program. */
                int x;
                {
                    x = foo()
                }
            """
            ast = self.build_ast(source_string)
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)

    @unittest.skip("Semantic check for function signatures not implemented yet")
    def test_semantic_declared_function_wrong_number_arguments(self):
        with self.assertRaises(UndeclaredFunctionError):
            source_string = """
                /* Declare a function named 'fum', with two arguments. */
                fum(y, z); { return y + z; }

                /* Call function 'fum' with one argument. */
                int x;
                {
                    x = fum(9)
                }
            """
            ast = self.build_ast(source_string)
            analyzer = DLSemanticAnalyzer()
            result = analyzer.analyze(ast)


    @unittest.skip("Inferred type for variables not implemented yet")
    def test_semantic_function_declaration_one_argument_one_variable(self):
        source_string = """
            /* Declare a function named 'bar', with one argument. */
            bar(x); { return x * 10; }

            /* Call 'bar' in the main body of the program. */
            int y;
            {
                y = bar(5)
            }
        """
        ast = self.build_ast(source_string)
        analyzer = DLSemanticAnalyzer()
        result = analyzer.analyze(ast)

        self.assertEqual(str(result.declarations), "Declarations(FunctionDeclaration(bar, Arguments(Variable(x)), Block(Return(BinOp(MULTIPLYOP, Variable(x), Integer(10))))), VariableDeclarations(INT, Variable(y)))")
        self.assertEqual(str(result.body), "Block(Assign(Variable(y), FunctionCall(bar, Arguments(Integer(5)))))")


    @unittest.skip("Inferred type for variables not implemented yet")
    def test_semantic_function_declaration_with_variables(self):
        source_string = """
            /* Declare a function named 'baz', with a variable declaration. */
            baz();
            int x;
            {
                return x + 2
            }

            /* Call 'baz' in the main body of the program. */
            int y;
            {
                y = baz()
            }
        """
        ast = self.build_ast(source_string)
        analyzer = DLSemanticAnalyzer()
        result = analyzer.analyze(ast)

        self.assertEqual(str(result.body), "Block(Assign(Variable(y), FunctionCall(baz)))")

        decs = result.declarations
        func = decs.declarations[0]
        self.assertEqual(func.name, "baz")
        self.assertEqual(func.args, None)
        self.assertEqual(str(func.vars), "VariableDeclarations(INT, Variable(x))")
        self.assertEqual(str(func.body), "Block(Return(BinOp(PLUSOP, Variable(x), Integer(2))))")


    @unittest.skip("Inferred type for variables not implemented yet")
    def test_semantic_code_example(self):
        source_file = open("tests/simple.dl",'r')
        source_string = source_file.read()
        source_file.close()

        ast = self.build_ast(source_string)
        analyzer = DLSemanticAnalyzer()
        result = analyzer.analyze(ast)

        decs = result.declarations
        func = decs.declarations[0]
        self.assertEqual(func.name, "factorial")
        self.assertEqual(str(func.args), "Arguments(Variable(n))")
        self.assertEqual(func.vars, None)

        conditional = func.body.statements[0]
        self.assertEqual(str(conditional.condition), "RelOp(EQOP, Variable(n), Integer(0))")
        self.assertEqual(str(conditional.body_true), "Block(Return(Integer(1)))")
        self.assertEqual(str(conditional.body_else), "Block(Return(BinOp(MULTIPLYOP, Variable(n), FunctionCall(factorial, Arguments(BinOp(MINUSOP, Variable(n), Integer(1)))))))")


        main_vars = decs.declarations[1]
        self.assertEqual(str(main_vars), "VariableDeclarations(INT, Variable(x))")

        main = result.body
        first = main.statements[0]
        self.assertEqual(str(first), "Assign(Variable(x), Integer(1))")
        second = main.statements[1]
        self.assertEqual(str(second.condition), "RelOp(LEOP, Variable(x), Integer(10))")
        self.assertEqual(str(second.body), "Block(Print(FunctionCall(factorial, Arguments(Variable(x)))), Assign(Variable(x), BinOp(PLUSOP, Variable(x), Integer(1))))")

    def build_ast(self, source):
        """A helper function to perform repeated test steps."""
        lexer = DLLexer()
        parser = DLParser()

        tokens = lexer.tokenize(source)
        ast = parser.parse(tokens)
        return ast


if __name__ == '__main__':
    unittest.main()
