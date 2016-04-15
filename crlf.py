#!/usr/bin/env python3
import os
import sys
import io
crlf = b'\r\n'
lf = b'\n'
cr =  b'\r'

dic = {
    'crlf'  : crlf,
    'win'   : crlf,
    'cr'    : cr,
    'mac'   : cr,
    'lf'    : lf,
    'unix'  : lf,
    'linux' : lf

    }
if (len(sys.argv) < 3):
    tab = ' '*4
    
    print("Syntax:")
    print(tab+"crlf.py file target [-o] [output]")
    print("")
    print("target:")
    print("-CR or -mac             convert LF and CRLF to Macintosh compatible CR")
    print("-LF or -unix or -linux  convert CR and CRLF to Linux and Unix compatible CR")
    print("-CRLF or -win           convert LF and CR to Windows compatible CRLF")

else:

    inFile = None
    outFile = None
    target = None
    overwrite = False
    for arg in sys.argv[1:]: # skip first argument, which is the path of this script.
        if arg[0] == '-' or arg[0] == '/':
            arg = arg[1:].lower()
            if arg == 'o':
                overwrite = True
            elif arg in dic:
                if target is None:
                    target = dic[arg]
                else:
                    print("Cannot set target line endings twice.")
                    exit(-1)
        else:
            if inFile is None:
                inFile = arg
            elif outFile is None:
                outFile = arg
            else:
                print("");
                exit(-2)
    #validation
    if target is None:
        print("No line ending specified")
        exit(-3)
        
    if inFile is None:
        print("No valid target platform provided")
        exit(-4)
    if False == os.path.exists(inFile):
        print("Input file does not exist")
        exit(-5)

    if outFile is None:
        outFile = inFile
        overwrite = True
    elif os.path.exists(outFile) and not overwrite:
        print("Output file exists. Please add overwrite flag ( -o ).")
        exit(-6)
        

    
    buffer = io.BytesIO()

    
    handle = open(inFile, 'rb+')
    prev = None
    current = handle.read(1)
    while(current != b""):
        if(current == b'\r'):
            buffer.write(target)
        elif (current == b'\n'):
            if(prev != b'\r'): #skip if it's \r\n, because we've already replaced it
                buffer.write(target)
        else:
            buffer.write(current)
        prev = current
        current = handle.read(1)
        
    #end of while
    if(inFile == outFile):
        handle.seek(0)
        handle.truncate()
    else:
        handle.close()
        handle = open(outFile, 'rb+');
        handle.truncate()
    
    handle.write(buffer.getvalue())
    handle.close()

