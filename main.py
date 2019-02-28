import rlexer
import rparser
import rassembler

import tkinter as tk
from tkinter.filedialog import askopenfilename

def main():
    tk.Tk().withdraw()
    path = askopenfilename()
    file = open(path, 'r')
    data = "".join(file.readlines())
    tokens = rlexer.Lexer(data).lex()
    ast = rparser.Parser(tokens).parse()
    rassembler.Assembler(open("a.asm",'w')).compile(ast)


if __name__ == "__main__":
    main()
