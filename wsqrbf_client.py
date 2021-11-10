#!/usr/bin/python
#
# Web Service & Quick Response based Brainfuck interpreter/client
#
# Usage: ./wsqrbf_client.py [FILE]

import sys
import io
import qrtools
from PIL import Image


def execute(filename):
    f = open(filename, "r")
    evaluate(f.read())
    f.close()


def evaluate(code):
    code = code.split('§')


def decode_qr(encoded_string):
    pass


def extract_data(qr):
    pass
    #io.BytesIO()
    #Image.frombytes()


def main():
    if len(sys.argv) == 2:
        execute(sys.argv[1])
    else:
        print("Usage:", sys.argv[0], "filename")


if __name__ == "__main__": main()


