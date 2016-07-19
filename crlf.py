#!/usr/bin/env python3
import os
import sys
import io
import argparse

class LineEndings:
    overwrite = False
    symbol = None
    
    def process(self, inFile, outFile):
        buffer = io.BytesIO()
        handle = open(inFile, 'rb+')
        prev = None
        current = handle.read(1)
        while(current != b""):
            if(current == b'\r'):
                buffer.write(self.symbol)
            elif (current == b'\n'):
                if(prev != b'\r'): #skip if it's \r\n, because we've already replaced it
                    buffer.write(self.symbol)
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
            handle = open(outFile, 'w+');
            handle.truncate()
        
        handle.write(buffer.getvalue())
        handle.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts the line endings of a file. Author: By Niek Hoekstra',)
    parser.add_argument('ending', help='New line endings', choices=['cr', 'lf', 'crlf', 'win','linux', 'mac'])
    parser.add_argument('input', help='File to adjust line endings of.')
    parser.add_argument('-o', '--output', help='Output file', default=None)
    parser.add_argument('--overwrite', help='Overwrite the current file or the output file.', action='store_true', default=False)

    args = parser.parse_args()

    editor = LineEndings()
    if not os.path.exists(args.input):
        print('Input file does not exist')
        exit(-1)

    if args.output is None:
        args.output = args.input

    if os.path.exists(args.output):
        if not args.overwrite:
            print('Output already exists, please use the overwrite flag to continue')
            exit(-1)
            
    _dic = {
        'win'   : b'\r\n',
        'crlf'  : b'\r\n',
        
        'linux' : b'\n',
        'unix'  : b'\n',
        'lf'    : b'\n',

        'mac'   : b'\r',
        'cr'    : b'\r'
        }
    editor.symbol = _dic[args.ending]
    editor.overwrite = args.overwrite
    editor.process(args.input, args.output)
