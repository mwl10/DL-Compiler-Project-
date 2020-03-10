import sys

from dl.lexer import DLLexer
from dl.parser import DLParser
from dl.semantic import DLSemanticAnalyzer
from dl.generator import DLGenerator

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("usage: generator.py <filename>")
    filename = sys.argv[1]

    infile = open(filename, "r")
    text = infile.read()
    infile.close()
    text.rstrip()

    if text:
        lexer = DLLexer()
        parser = DLParser()
        semantic = DLSemanticAnalyzer()
        generator = DLGenerator()
        tokens = lexer.tokenize(text)
        ast = parser.parse(tokens)
        checked = semantic.analyze(ast)
        ir = generator.generate(checked)
        if ir:
            outname = filename.replace(".dl", ".ll")
            outfile = open(outname, "w")
            outfile.write(ir)
            outfile.close()
            print("Wrote output file:", outname)
