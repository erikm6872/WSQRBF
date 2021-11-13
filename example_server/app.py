from flask import Flask

"""
Web Service & Quick Response based Brainfuck Server

Usage: ./flask run

TODO: Encapsulate response text in SOAP messages to increase the number of bytes transferred per request
"""


app = Flask(__name__)


@app.route("/ip")
def increment_pointer():
    return "self.cellptr += 1\nif self.cellptr == len(self.cells): self.cells.append(0)"


@app.route("/dp")
def decrement_pointer():
    return "self.cellptr = 0 if self.cellptr <= 0 else self.cellptr - 1"


@app.route("/iv")
def increment_value():
    return "self.cells[self.cellptr] = self.cells[self.cellptr] + 1 if self.cells[self.cellptr] < 255 else 0"


@app.route("/dv")
def decrement_value():
    return "self.cells[self.cellptr] = self.cells[self.cellptr] - 1 if self.cells[self.cellptr] > 0 else 255"


@app.route("/o")
def output_value():
    return "sys.stdout.write(chr(self.cells[self.cellptr]))"


@app.route("/in")
def take_input():
    return "self.cells[self.cellptr] = ord(msvcrt.getch())"


@app.route("/jf")
def jump_forward():
    """
    The jump commands are a bit odd here. We need to give the client some way to identify the [ and ] commands
    so that we can build a map for the matching brackets as the responses come in. Starting the response msg with &jf
    lets us identify it as a jump. TODO: Figure out a better way to do this. Maybe an obscure HTTP status or something.
    """
    return """&jf
if self.cells[self.cellptr] == 0:\n
\tself.codeptr = self.bracemap[self.codeptr]"""


@app.route("/jb")
def jump_back():
    return """&jb
if self.cells[self.cellptr] != 0:\n
\tself.codeptr = self.bracemap[self.codeptr]"""
