# WSQRBF

### Overview

**Web Service & Quick Response based Brainfuck** is an 
[esoteric programming language](https://en.wikipedia.org/wiki/Esoteric_programming_language)
based on 
[Brainfuck](https://en.wikipedia.org/wiki/Brainfuck). 
However, there are several notable differences:

* Instructions consist of a URL and a GUID embedded in a QR code 
image, which is then encoded in Base64. For this reason, WSQRBF source files
are _not_ human readable and are more than 29 million times larger than an 
equivalent brainfuck source.

* For every instruction, the interpreter must query the API endpoint specified
by the embedded URL to determine the instruction's behavior. The response 
consists of a SOAP message containing Python code, which the interpreter 
executes blindly without sanitation of any kind. 

* This means that the behavior of a given instruction can change without warning,
_even in the middle of execution_. Implementations of the API are encouraged
to remain closed source and completely undocumented.

    - Also note that because of the considerable security risks involved, use 
    of HTTPS or any other protocol that supports encryption is strictly 
    prohibited.

### Source Files

Source files are **UCS-2 LE BOM encoded** plain text files and use the _.wsqrbf_ 
file extension. The procedure for writing a WSQRBF program is as follows:

1. Find the URL for the API endpoint corresponding to the first instruction. 
    
    - This may be more difficult than it seems. Endpoints may be given any 
    valid URL and the routing may change at any time.
    
2. Generate a PNG format QR code image containing the URL and a 16 byte hex GUID. 

    - To prevent code re-use, this GUID **must** be unique for every instruction in the program.
    A single duplicate GUID will cause the program to immediately terminate with an error code.

3. Encode the PNG bytes as a Base64 string. This string represents exactly one instruction
and cannot be reused as the GUID will not be unique.

4. Repeat for every instruction in the program. Instruction strings are separated by the 
`§` character (U+00A7).

### Example source

TODO

### API Behavior

TODO

### Interpreter/Client
Usage: `./wsqrbf_client.py [FILE]`

Note that this interpreter is not currently functional in any capacity.