import sys
import msvcrt

DEBUG = False   # Set to True to enable debugging message output
JUMP_FORWARD = "&jf"
JUMP_BACKWARD = "&jb"

class Machine:
    """
    Main BF machine. Logic is (loosely) based on https://github.com/pocmo/Python-Brainfuck/blob/master/brainfuck.py
    """

    def __init__(self):
        self.cells = [0]
        self.cellptr = 0
        self.codeptr = 0
        self.bracemap = {}
        self.bracestack = []
        self.execution_list = []

    def __enter__(self):
        return self

    def add_command(self, code):
        """Add command to list. We need to perform a few extra operations to enable the jump instructions"""
        if code[:3] == JUMP_FORWARD:
            self.bracestack.append(len(self.execution_list))
            code = code[4:]
        elif code[:3] == JUMP_BACKWARD:
            start = self.bracestack.pop()
            self.bracemap[start] = len(self.execution_list)
            self.bracemap[len(self.execution_list)] = start
            code = code[4:]
        self.execution_list.append(code)

    def execute(self):
        """Reset the pointer to 0, then iterate over the exec list and execute all instructions"""
        self.codeptr = 0
        while self.codeptr < len(self.execution_list):
            exec(self.execution_list[self.codeptr])
            self.codeptr += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        if DEBUG:
            print("Final: " + repr(vars(self)))
