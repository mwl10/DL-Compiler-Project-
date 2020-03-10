import unittest

import subprocess
import os
import sys
sys.path.append('.')


from dl.lexer import DLLexer
from dl.parser import DLParser
from dl.semantic import DLSemanticAnalyzer
from dl.generator import DLGenerator

class TestGenerator(unittest.TestCase):

    def test_generate_integer_constant(self):
        ir = self.generate('{ print(3) }')
        result = self.execute_llvm(ir)
        self.assertEqual(result, "3")

    def test_generate_addition_integer_constant(self):
        ir = self.generate('{ print(5 + 7) }')
        result = self.execute_llvm(ir)
        self.assertEqual(result, "12")

    def test_generate_subtraction_integer_constant(self):
        ir = self.generate('{ print(10 - 2) }')
        result = self.execute_llvm(ir)
        self.assertEqual(result, "8")

    def test_generate_multiplication_integer_constant(self):
        ir = self.generate('{ print(6 * 5) }')
        result = self.execute_llvm(ir)
        self.assertEqual(result, "30")

    def test_generate_division_integer_constant(self):
        ir = self.generate('{ print(12 / 6) }')
        result = self.execute_llvm(ir)
        self.assertEqual(result, "2")

    def test_generate_declared_variable_print(self):
        source_string = """
            int a;
            {
                print(a)
            }
        """
        ir = self.generate(source_string)
        result = self.execute_llvm(ir)
        self.assertEqual(result, "0")

    def test_generate_addition_declared_variable(self):
        source_string = """
            int b;
            {
                print(b + 3)
            }
        """
        ir = self.generate(source_string)
        result = self.execute_llvm(ir)
        self.assertEqual(result, "3")


    def test_generate_assignment_statement(self):
        source_string = """
            int c;
            {
                c = 6;
                print(c)
            }
        """
        ir = self.generate(source_string)
        result = self.execute_llvm(ir)
        self.assertEqual(result, "6")


    def test_generate_declared_array_assign(self):
        source_string = """
            int d[10], e;
            {
                d[5] = 7;
                e = d[5];
                print(e)
            }
        """
        ir = self.generate(source_string)
        result = self.execute_llvm(ir)
        self.assertEqual(result, "7")

    def test_generate_read_statement(self):
        source_string = """
            int f;
            {
                read(f);
                print(f)
            }
        """
        ir = self.generate(source_string)
        result = self.execute_llvm_read(ir, "78")
        self.assertEqual(result, "78")

    def test_generate_if_gt(self):
        source_string = """
            int q, r, s;
            {
                q = 5;
                r = 11;
                s = 22;
                if (q > 1) { print(r) }
                else { print(s) }
            }
        """
        ir = self.generate(source_string)
        result = self.execute_llvm(ir)
        self.assertEqual(result, "11")

    def test_generate_if_ge(self):
        source_string = """
            int q, r;
            {
                q = 5;
                r = 22;
                if (q >= 4) { print(r) }
            }
        """
        ir = self.generate(source_string)
        result = self.execute_llvm(ir)
        self.assertEqual(result, "22")

    def test_generate_if_lt(self):
        source_string = """
            int q, r, s;
            {
                q = 12;
                r = 33;
                s = 44;
                if (q < 10) { print(r) }
                else { print(s) }
            }
        """
        ir = self.generate(source_string)
        result = self.execute_llvm(ir)
        self.assertEqual(result, "44")

    def test_generate_if_le(self):
        source_string = """
            int q, r;
            {
                q = 10;
                r = 3;
                if (q <= 10) { print(r) }
            }
        """
        ir = self.generate(source_string)
        result = self.execute_llvm(ir)
        self.assertEqual(result, "3")

    def test_generate_if_eq(self):
        source_string = """
            int q, r;
            {
                q = 20;
                r = 66;
                if (q == 20) { print(r) }
            }
        """
        ir = self.generate(source_string)
        result = self.execute_llvm(ir)
        self.assertEqual(result, "66")

    def test_generate_if_ne(self):
        source_string = """
            int q, r;
            {
                q = 7;
                r = 77;
                if (q != 14) { print(r) }
            }
        """
        ir = self.generate(source_string)
        result = self.execute_llvm(ir)
        self.assertEqual(result, "77")

    def test_generate_while_lt(self):
        source_string = """
            int t;
            {
                t = 1;
                while(t < 10) {
                    t = t + 1;
                };
                print(t);
            }
        """
        ir = self.generate(source_string)
        result = self.execute_llvm(ir)
        self.assertEqual(result, "10")

    def test_generate_function_no_arguments(self):
        source_string = """
            /* Declare a function named 'foo'. */
            foo();
            {
                return 22
            }
            /* Call 'foo' in the main body of the program. */
            int x;
            {
                x = foo();
                print(x)
            }
        """
        ir = self.generate(source_string)
        result = self.execute_llvm(ir)
        self.assertEqual(result, "22")

    def test_generate_function_one_argument(self):
        source_string = """
            /* Declare a function named 'bar'. */
            bar(x);
            {
                return x * 5
            }
            /* Call 'bar' in the main body of the program. */
            int y;
            {
                y = bar(4);
                print(y)
            }
        """
        ir = self.generate(source_string)
        result = self.execute_llvm(ir)
        self.assertEqual(result, "20")

    def test_generate_function_multiple_arguments(self):
        source_string = """
            /* Declare a function named 'baz'. */
            baz(x, y, z);
            int q;
            {
                q = x + y;
                q = q * z;
                return q
            }
            /* Call 'baz' in the main body of the program. */
            int a, b;
            {
                a = 6;
                b = baz(a, 2, 3);
                print(b)
            }
        """
        ir = self.generate(source_string)
        result = self.execute_llvm(ir)
        self.assertEqual(result, "24")

    def test_generator_code_example(self):
        source_file = open("tests/simple2.dl",'r')
        source_string = source_file.read()
        source_file.close()

        ir = self.generate(source_string)
        result = self.execute_llvm(ir)
        expected = "1\n2\n6\n24\n120\n720\n5040\n40320\n362880\n3628800"
        self.assertEqual(result, expected)


    def generate(self, source):
        lexer = DLLexer()
        parser = DLParser()
        semantic = DLSemanticAnalyzer()
        generator = DLGenerator()

        tokens = lexer.tokenize(source)
        ast = parser.parse(tokens)
        checked = semantic.analyze(ast)
        ir = generator.generate(checked)
        return ir

    def execute_llvm(self, ir):
        if ir:
            outfile = open('test_tmp.ll', "w")
            outfile.write(ir)
            outfile.close()
            runner = os.popen('/usr/local/opt/llvm/bin/lli test_tmp.ll')
            result = runner.read()
            runner.close()
            os.remove('test_tmp.ll')
            result = result.rstrip()
        return result

    def execute_llvm_read(self, ir, content):
        read_input = (content + '\nEOF').encode('utf-8')
        if ir:
            outfile = open('test_tmp.ll', "w")
            outfile.write(ir)
            outfile.close()
            result = subprocess.run(["/usr/local/opt/llvm/bin/lli", "test_tmp.ll"], input=read_input, stdout=subprocess.PIPE)
            os.remove('test_tmp.ll')
            output = result.stdout.decode('utf-8').rstrip()
        return output

if __name__ == '__main__':
    unittest.main()
