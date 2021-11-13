#!/usr/bin/python
#
# Web Service & Quick Response based Brainfuck interpreter/client
#
# Usage: ./wsqrbf_client.py [FILE]

import sys
import io
import base64
import pyqrcode
import requests
from PIL import Image
from pyzbar.pyzbar import decode

from Machine import Machine
from StoredQRData import StoredQRData

SEP_CHAR = '~'
VALIDATE_ENCODE = False
SHOW_QR = False


def execute_file(filename):
    """Open source file and execute"""
    f = open(filename, "r", encoding='utf-16')
    evaluate(f.read())
    f.close()


def evaluate(code):
    """
    evaluate
    TODO: Figure out if it is possible to execute code as it is received. The jump command behavior doesn't seem to
    allow this, but there might be a way using queues.
    """
    code = code.split(SEP_CHAR)
    guids = []
    with Machine() as machine:
        for x in code:
            if x != '':
                y = x.strip(SEP_CHAR)  # strip ~ if split didn't do it
                qr_data = decode_qr(y)
                if qr_data.guid not in guids:   # GUIDs must be unique for every individual command
                    guids.append(qr_data.guid)
                    call_api(qr_data.url, machine)
                else:
                    print("ERROR! Duplicate GUIDs. Exiting.")   # TODO: Make this an exception
                    sys.exit(1)
            else:
                machine.execute()   # After all commands are in execution list, execute the program.

def decode_qr(encoded_string):
    """decode_qr"""
    decoded_str = base64.b64decode(encoded_string)
    qr_data = extract_data(decoded_str)
    return qr_data


def extract_data(qr):
    """extract qr code data"""
    img_bytes = io.BytesIO(qr)
    try:
        img = Image.open(img_bytes)
    except:
        return StoredQRData()
    # img.show()        # open every QR image being processed in the default app for PNGs
    decoded = decode(img)
    data_str = decoded[0].data.decode('ascii')
    data_list = data_str.split('~')
    qr_data = StoredQRData(data_list[0], data_list[1])
    return qr_data


def call_api(url, machine=None):
    """
    Perform a GET call to the specified URL, then add the response text to the BF machine's command list.
    TODO: Implement SOAP to increase bytes transferred per request
    """
    response = requests.get(url)
    if machine:
        machine.add_command(response.text)
    else:
        print(response.text)


def encode_instruction(url):
    """encode_instruction"""
    qr_data = StoredQRData(url)
    qrcode = pyqrcode.create(url + SEP_CHAR + repr(qr_data.guid))
    enc_qr = qrcode.png_as_base64_str(scale=10)

    if VALIDATE_ENCODE:
        # Validate that the newly encoded string also decodes properly
        dec = decode_qr(enc_qr)
        if qr_data != dec:
            print("ERROR: " + repr(qr_data) + " != " + repr(dec))   # TODO: Change this to an exception
    return enc_qr


def encode_bf(bf):
    """encode brainfuck code to WSQRBF"""
    # These are the API endpoints for the example server running on localhost. Replace them with your server's URLs.
    cmds = {
        '>': 'http://127.0.0.1:5000/ip',
        '<': 'http://127.0.0.1:5000/dp',
        '+': 'http://127.0.0.1:5000/iv',
        '-': 'http://127.0.0.1:5000/dv',
        '.': 'http://127.0.0.1:5000/o',
        ',': 'http://127.0.0.1:5000/in',
        '[': 'http://127.0.0.1:5000/jf',
        ']': 'http://127.0.0.1:5000/jb',
            }
    src = ""
    for x in bf:
        if x in cmds:
            enc_qr = encode_instruction(cmds[x])
            src = src + enc_qr + SEP_CHAR
        else:
            raise RuntimeError("Char '" + x + "' is not a valid Brainfuck command")
    return src


def encode_file(filename, outfile=None):
    """encode_file"""
    f = open(filename, "r")
    result = encode_bf(f.read())
    f.close()
    if outfile:
        f = open(outfile, "w", encoding='utf-16')
        f.write(result)
        f.close()
        print("Encoded data written to " + outfile)
    else:
        print(result)


def main():
    """
    main method
    TODO: argparse
    """
    if len(sys.argv) == 2:
        execute_file(sys.argv[1])
    elif len(sys.argv) == 3:
        if sys.argv[1] == "enc":
            encode_instruction(sys.argv[2])
        elif sys.argv[1] == "enc_str":
            encode_bf(sys.argv[2])
        elif sys.argv[1] == "enc_file":
            encode_file(sys.argv[2])
        elif sys.argv[1] == "call":
            call_api(sys.argv[2])
        else:
            print("Unknown arg")
    elif len(sys.argv) == 4:
        if sys.argv[1] == "enc_file":
            encode_file(sys.argv[2], sys.argv[3])
    else:
        print("Usage:", sys.argv[0], "filename")


if __name__ == "__main__":
    main()
