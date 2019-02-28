import sys

from rparser import NodeType


class Assembler:
    def __init__(self, output_file=sys.stdout):
        self.output_file = output_file
        self.batch = []
        self.table = {"eax": False, "ebx":False,  "ecx": False, "edx": False}

    def compile(self, node):
        self.visit(node)
        self.footer()
        self.flush()

    def visit(self, node):
        self.flush()
        # print(node.value)
        if node.node_type == NodeType.DECLARE:
            self.header()
            # print("header")
            for n in node.children:
                self.visit(n)
        elif node.node_type == NodeType.VARIABLE:
            # print("var", node.value)
            self.visit_var(node)
        elif node.node_type == NodeType.NUMBER:
            # print("num", node.value)
            if not self.table.get("ecx"):
                self.visit_num(node, "ecx")
                self.table.update({"ecx": True})
            elif not self.table.get("edx"):
                self.visit_num(node, "edx")
                self.table.update({"edx": True})
            elif not self.table.get("ebx"):
                self.visit_num(node, "ebx")
                self.table.update({"ebx": True})
            elif not self.table.get("eax"):
                self.visit_num(node, "eax")
                self.table.update({"eax": True})
            else:
                print("Out of registers!", file=sys.stderr)
                exit()
        elif node.node_type == NodeType.BIN:

            for n in node.children:
                self.visit(n)
            # print("op", node.value)
            self.visit_bin_op(node)
        elif node.node_type == NodeType.CALL:
            for n in node.children:
                self.visit(n)
            # print("call", node.value)
            self.visit_call(node)
        self.flush()

    def visit_bin_op(self, node):
        # print("visit bin", node.value)
        value = node.value
        ops = {'+': "add", '-': "sub", '*': "imul"}
        try:
            op = ops.get(value)
            self.instr(op, node.children[0].reg, node.children[1].reg)
            self.use(node.children[1].reg)
            node.set_reg(node.children[0].reg)
        except:
            print("Operation not supported yet!", file=sys.stderr)
            exit()

    def visit_num(self, node, reg):
        # print("visit num", node.value)
        node.set_reg(reg)
        # print(node.reg)
        self.instr("mov", reg, node.value)

    def use(self, reg):
        self.table.update({reg: False})

    def visit_var(self, node):
        # print("visit var")
        if node.value == "main":
            self.directive("_main:")

    def visit_call(self, node):
        # print("visit call")
        value = node.value
        if value == "print":
            if node.children[0].node_type == NodeType.NUMBER:
                self.use(node.children[0].reg)
            self.instr("push", node.children[0].reg)
            self.use(node.children[0].reg)
            self.instr("push", "out")
            self.instr("call", "_printf")
            self.instr("add", "esp", "4")
            # self.instr("mov", "DL", "0DH")
            # self.instr("mov", "DL", "0AH")
            # self.instr("int", "21H")

    def write(self, data):
        print(data, file=self.output_file)

    def flush(self):
        try:
            for op, args in self.batch:
                self.write("\t%s    %s" % (op, ", ".join(args)))
            self.batch = []
        except:
            print(*self.batch, sep='\n')
            self.batch = []
            exit()
            pass

    def header(self):
        self.directive("\tglobal _main")
        self.directive("\textern _printf")
        self.directive("\tsection .text")

    def footer(self):
        self.directive("    ret")
        self.directive("out:")
        self.instr("db", '"%d"', "0DH", "0AH", "0")

    def directive(self, line):
        self.flush()
        self.write(line)

    def instr(self, instruction, *args):
        self.batch.append((instruction, args))
