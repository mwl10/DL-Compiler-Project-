from dl.visitor import ASTVisitor
from dl.ast import Variable, ArrayIndex, VariableDeclarations, FunctionDeclaration
from dl.symbols import VariableSymbol, ArgumentSymbol, ArraySymbol

class DLGenerator(ASTVisitor):
    """Generate LLVM code from an AST.
    Traverse an abstract syntax tree (AST) with recursive descent, and
    generate LLVM code corresponding to the source program.
    Attributes:
        code -- collects lines of generated code
        reg_count -- current count of temporary registers
        label_count -- current count of unique labels
    """
    def __init__(self):
        self.code = []
        self.reg_count = 0
        self.label_count = 0

    def add_code(self, lines):
        """Add some lines of generated code."""
        if self.code:
            self.code.append(lines)
        else:
            self.code = [lines]

    def new_temporary(self):
        """Create a new temporary register."""
        self.reg_count += 1
        name = "%tmp." + str(self.reg_count)
        return name

    def new_label(self, partial):
        """Create a new unique label."""
        self.label_count += 1
        label = partial + "." + str(self.label_count)
        return label

    def generate(self, program):
        """Begin generation on the top-level node."""
        self.visit(program)

        # Squash all the lines of code into a single string
        ir = "\n".join(self.code)
        return ir


    def visit_Integer(self, node):
        """Call the generator for Expr AST nodes."""
        return str(node.value)


    def visit_Variable(self, node):
        """Call the generator for Variable AST nodes."""
        if isinstance(node.symbol, VariableSymbol):
            return self.access_Variable(node)
        elif isinstance(node.symbol, ArgumentSymbol):
            return self.access_Argument(node)
        else:
            raise GeneratorError("Attempt to access undeclared variable symbol: " + node.name)

    def access_Variable(self, node):
        """Call the generator for Variable AST nodes, containing local variables."""
        temp_name = self.new_temporary()
        local_name = "%" + node.name
        template = """
            %s = load i32, i32* %s
                    """
        output_code = template % (temp_name, local_name)
        self.add_code(output_code)
        return temp_name


    def access_Argument(self, node):
        """Call the generator for Variable AST nodes, containing function arguments."""
        return "%" + node.name


    def visit_ArrayIndex(self, node):
        """Call the generator for Variable AST nodes."""
        symbol = node.symbol
        array_size = 0
        if symbol and isinstance(symbol, ArraySymbol):
            array_size = symbol.size.value
        else:
            raise GeneratorError("Use of array with unknown size: " + node.var.name)

        temp_pointer = self.new_temporary()
        temp_value = self.new_temporary()
        template = """
    %s = getelementptr [%s x i32], [%s x i32]* %s, i32 0, i32 %s
    %s = load i32, i32* %s
        """
        local_name = "%" + node.var.name
        array_index = node.index.value
        output_code = template % (temp_pointer, array_size, array_size, local_name, array_index, temp_value, temp_pointer)
        self.add_code(output_code)
        return temp_value


    def visit_BinOp(self, node):
        """Call the generator for BinOp AST nodes."""
        temp_name = self.new_temporary()
        opcode_name = ""
        if node.op == 'PLUSOP':
            opcode_name = "add"
        elif node.op == 'MINUSOP':
            opcode_name = "sub"
        elif node.op == 'MULTIPLYOP':
            opcode_name = "mul"
        elif node.op == 'DIVIDEOP':
            opcode_name = "udiv"

        left_reg = self.visit(node.left)
        right_reg = self.visit(node.right)

        template = """
            %s = %s i32 %s, %s
        """
        output_code = template % (temp_name, opcode_name, left_reg, right_reg)
        self.add_code(output_code)
        return temp_name

    def visit_RelOp(self, node):
        """Call the generator for RelOp AST nodes."""
        temp_name = self.new_temporary()
        opcode_name = ""
        if node.op == 'EQOP':
            opcode_name = "eq"
        elif node.op == 'NEOP':
            opcode_name = "ne"
        elif node.op == 'LTOP':
            opcode_name = "slt"
        elif node.op == 'LEOP':
            opcode_name = "sle"
        elif node.op == 'GTOP':
            opcode_name = "sgt"
        elif node.op == 'GEOP':
            opcode_name = "sge"

        left_reg = self.visit(node.left)
        right_reg = self.visit(node.right)

        template = """
    %s = icmp %s i32 %s, %s
        """
        output_code = template % (temp_name, opcode_name, left_reg, right_reg)
        self.add_code(output_code)
        return temp_name


    def visit_FunctionCall(self, node):
        """Call the generator for FunctionCall AST nodes."""
        # %tmp.7 = call i32 @alpha(i32 %tmp.8, i32 %tmp.9)
        temp_name = self.new_temporary()
        function_name = "@" + node.name

        args_string = ""
        if node.args:
            args_string = self.visit(node.args)

        template = """
        %s = call i32 %s(%s)
        """

        output_code = template % (temp_name, function_name, args_string)
        self.add_code(output_code)
        return temp_name

    def visit_Arguments(self, node):
        """Call the generator for Arguments AST nodes."""
        argument_list = []
        for argument in node.arguments:
            arg_name = self.visit(argument)
            argument_list.append("i32 " + arg_name)
        return ", ".join(argument_list)


    def visit_Assign(self, node):
        """Call the generator for Assign AST nodes."""
        right_reg = self.visit(node.right)

        if isinstance(node.left, Variable):
            self.assign_Variable(node.left, right_reg)
        elif isinstance(node.left, ArrayIndex):
            self.assign_ArrayIndex(node.left, right_reg)
        else:
            raise GeneratorError("Assignment is only possible to variables and indexed array elements")

    def assign_Variable(self, node, right_reg):
        """Call the generator for assignment to Variable AST nodes."""
        symbol = node.symbol
        template = """
            store i32 %s, i32* %s
        """
        local_name = "%" + node.name
        output_code = template % (right_reg, local_name)
        self.add_code(output_code)

    def assign_ArrayIndex(self, node, right_reg):
        """Call the generator for assignment to ArrayIndex AST nodes."""
        symbol = node.symbol
        array_size = 0
        if symbol and isinstance(symbol, ArraySymbol):
            array_size = symbol.size.value
        else:
            raise GeneratorError("Use of array with unknown size: " + node.var.name)

        temp_pointer = self.new_temporary()
        template = """
    %s = getelementptr [%s x i32], [%s x i32]* %s, i32 0, i32 %s
    store i32 %s, i32* %s
        """
        local_name = "%" + node.var.name
        array_index = node.index.value
        output_code = template % (temp_pointer, array_size, array_size, local_name, array_index, right_reg, temp_pointer)
        self.add_code(output_code)


    def visit_Print(self, node):
        """Call the generator for Print AST nodes."""
        print_val = self.visit(node.arg)
        template = """
    call i32 (i8*, ...) @printf(i8* getelementptr([4 x i8], [4 x i8]* @.formatstr, i32 0, i32 0), i32 %s)
        """
        output_code = template % (print_val)
        self.add_code(output_code)


    def visit_Read(self, node):
        """Call the generator for Read AST nodes."""
        result_reg = "%" + node.result.name
        template = """
    call i32 (i8*, ...) @scanf(i8* getelementptr([4 x i8], [4 x i8]* @.formatstr, i32 0, i32 0), i32* %s)
        """
        output_code = template % (result_reg)
        self.add_code(output_code)


    def visit_Return(self, node):
        """Call the generator for Return AST nodes."""
        result_reg = self.visit(node.result)
        template = """
    ret i32 %s
        """
        output_code = template % (result_reg)
        self.add_code(output_code)


    def visit_If(self, node):
        """Call the generator for If AST nodes."""
        end_label = self.new_label("if.end")
        true_label = self.new_label("if.true")
        false_label = self.new_label("if.false")

        # Output beginning label for the loop
        cond_reg = self.visit(node.condition)
        template = """
        br i1 %s, label %s, label %s
            %s:
                """
        output_code = template % (cond_reg, "%"+true_label, "%"+false_label, true_label)
        self.add_code(output_code)

        # Evaluate the conditions

        self.visit(node.body_true)
        # true body generated by visiting node.body_true
        template = """
            br label %s
                %s:
        """
        output_code = template % ("%"+end_label, false_label)
        self.add_code(output_code)

        if node.body_else:
            self.visit(node.body_else)
        # else body generated by visiting node.body_else
        template = """
        br label %s
            %s:
            """
        output_code = template % ("%" + end_label, end_label)
        self.add_code(output_code)


    def visit_While(self, node):
        """Call the generator for While AST nodes."""
        loop_label = self.new_label("while.loop")
        body_label = self.new_label("while.body")
        end_label = self.new_label("while.end")

        # Output beginning label for the loop
        template = """
    br label %s
  %s:
        """
        output_code = template % ("%"+loop_label, loop_label)
        self.add_code(output_code)

        # Evaluate the condition, before each iteration
        cond_reg = self.visit(node.condition)
        template = """
    br i1 %s, label %s, label %s
  %s:
        """
        output_code = template % (cond_reg, "%"+body_label, "%"+end_label, body_label)
        self.add_code(output_code)

        # Evaluate the loop body, after checking condition
        self.visit(node.body)
        template = """
    br label %s
  %s:
        """
        output_code = template % ("%"+loop_label, end_label)
        self.add_code(output_code)


    def visit_Block(self, node):
        """Call the generator for Block AST nodes."""
        for statement in node.statements:
            self.visit(statement)


    def visit_Declarations(self, node):
        """Call the generator for Declarations AST nodes."""
        variables = []
        for declaration in node.declarations:
            if isinstance(declaration, VariableDeclarations):
                variables.append(declaration)
            elif isinstance(declaration, FunctionDeclaration):
                self.visit(declaration)
        return variables


    def visit_VariableDeclarations(self, node):
        for declaration in node.variables:
            if isinstance(declaration, Variable):
                self.declare_Variable(declaration)
            elif isinstance(declaration, ArrayIndex):
                self.declare_ArrayIndex(declaration)
            else:
                raise GeneratorError("Declaration is only possible for variables and arrays")

    def declare_Variable(self, node):
        """Call the generator to declare variables."""
        template = """
    %s = alloca i32
    store i32 0, i32* %s
        """
        local_name = "%" + node.name
        output_code = template % (local_name, local_name)
        self.add_code(output_code)

    def declare_ArrayIndex(self, node):
        """Call the generator to declare arrays."""
        template = """
    %s = alloca [%s x i32]
        """
        local_name = "%" + node.var.name
        output_code = template % (local_name, node.index.value)
        self.add_code(output_code)


    def visit_FunctionDeclaration(self, node):
        """Call the generator for FunctionDeclaration AST nodes."""
        func_name = "@" + node.name
        args_string = ""

        if node.args:
            args_string = self.visit(node.args)

        template = """
define i32 %s(%s) {
  entry:
        """
        header = template % (func_name, args_string)
        self.add_code(header)

        if node.vars:
            self.visit(node.vars)

        self.visit(node.body)

        footer = """
}
        """
        self.add_code(footer)


    def visit_Program(self, node):
        """Call the generator for Program AST nodes."""
        var_decs = None
        if node.declarations:
            var_decs = self.visit(node.declarations)

        header = """
declare i32 @printf(i8*, ...) nounwind
declare i32 @scanf(i8*, ...)
@.formatstr = internal constant [4 x i8] c"%d\\0A\\00"
define i32 @main() {
  entry:
        """
        self.add_code(header)

        if var_decs:
            for variable in var_decs:
                self.visit(variable)

        self.visit(node.body)

        footer = """
    ret i32 0
}
        """
        self.add_code(footer)

class GenerationError(Exception):
    """Exception raised for errors detected in code generation.
    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
