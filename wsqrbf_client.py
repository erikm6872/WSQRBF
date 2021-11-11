#!/usr/bin/python
#
# Web Service & Quick Response based Brainfuck interpreter/client
#
# Usage: ./wsqrbf_client.py [FILE]

import sys
import io
import base64
import uuid
import pyqrcode
from PIL import Image
from pyzbar.pyzbar import decode
from base64 import decodestring

from StoredQRData import StoredQRData

SEP = '§'
A_SEP = '~'
VALIDATE_ENCODE = False


def execute(filename):
    f = open(filename, "r", encoding='utf-16')
    evaluate(f.read())
    f.close()


def evaluate(code):
    code = code.split(A_SEP)
    for x in code:
        x = x.strip(A_SEP)  # strip ~ if split didn't do it
        decode_qr(x)


def decode_qr(encoded_string):
    decoded_str = base64.b64decode(encoded_string)
    qr_data = extract_data(decoded_str)
    return qr_data


def extract_data(qr):
    img_bytes = io.BytesIO(qr)
    try:
        img = Image.open(img_bytes)
    except:
        pass
    img.show()
    decoded = decode(img)
    data_str = decoded[0].data.decode('ascii')
    data_list = data_str.split('~')
    qr_data = StoredQRData(data_list[0], data_list[1])
    #print(data_str)
    #print(repr(data_list))
    print("extract_data: " + repr(qr_data))
    return qr_data


def encode_instruction(url):
    qr_data = StoredQRData(url)
    qrcode = pyqrcode.create(url + A_SEP + repr(qr_data.guid))
    enc_qr = qrcode.png_as_base64_str(scale=10)

    if VALIDATE_ENCODE:
        dec = decode_qr(enc_qr)
        print("encode_inst: " + repr(qr_data))
        print()
        if qr_data == dec:
            print("ERROR")
            print()

    return enc_qr


def encode_bf(bf):
    cmds = {
        '>': 'http://localhost/ip',
        '<': 'http://localhost/dp',
        '+': 'http://localhost/iv',
        '-': 'http://localhost/dv',
        '.': 'http://localhost/o',
        ',': 'http://localhost/in',
        '[': 'http://localhost/jf',
        ']': 'http://localhost/jb',
            }
    src = ""
    for x in bf:
        #url = cmds[x]
        enc_qr = encode_instruction(cmds[x])
        src = src + enc_qr + A_SEP

        #decoded = decode_qr(enc_qr)


        #print(encode_instruction(cmds[x]))
    print(src)
    return src

def main():
    if len(sys.argv) == 2:
        execute(sys.argv[1])
    elif len(sys.argv) == 3:
        if sys.argv[1] == "enc":
            encode_instruction(sys.argv[2])
        elif sys.argv[1] == "enc_str":
            encode_bf(sys.argv[2])
        else:
            print("Unknown arg")
    else:
        print("Usage:", sys.argv[0], "filename")


if __name__ == "__main__": main()


