#!/usr/bin/env python3
import sys
import json
import fnmatch
import argparse

class JsonSearch:
    path = None
    value = None
    limit = None
    handler = None
    _count = 0

    def search(self, json):
        self._count = 0
        self._walk(json, [json], [])
        return

    def _walk(self, node, stack, path):
        for n in node:
            if(self._count == self.limit):
                return
            value = node[n]
            stack.append(value)
            if isinstance(value, dict):
                path.append(n)
                self._walk(value, stack, path)
                path.pop()
            elif isinstance(value, list):
                for i in range(0,len(value)):
                    if(self._count == self.limit):
                        return
                    path.append(n+'['+str(i)+']')
                    self._walk(value[i], stack, path)
                    path.pop()
            else:
                path.append(n)
                if(self._validate(value, path)):
                    self.handler(value, stack, path)
                    self._count += 1
                path.pop()
            stack.pop()

    def _validate(self, value, path):
        fullpath = '/'.join(path)
        return (self.path == None or fnmatch.fnmatch(fullpath, self.path)) and (self.value == None or self.value == value)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search JSON in path or for values. Author: By Niek Hoekstra')
    parser.add_argument('file', help='JSON file')

    parser.add_argument('-p', '--path', help='Search in JSON path, wildcards allowed. Example: */duration/value', default=None)
    parser.add_argument('-v', '--value', help='Search for value', default=None)
    parser.add_argument('-l', '--limit',  help='Limit the number of results', type=int, default=None)
    parser.add_argument('--type', help='Forces datatype for the value', choices=['int', 'float', 'string', 'auto'], default='auto')
    parser.add_argument('--print', help="print certain data, both by default", choices=['path', 'value', 'both'], default='both')
    parser.add_argument('--color', help="adds color to printed values", action='store_true', default=False)

    args = parser.parse_args()

    if(args.path == None and args.value == None):
        print('Must search path and/or value.')
        exit(-1)

    search = JsonSearch()
    search.path = args.path
    search.value = args.value
    search.limit = args.limit

    class printer:
        style_seperator = '/'
        style_text      = '\x1b[92m' #green
        style_number    = '\x1b[94m' #blue
        style_pathLeft  = '\x1b[2m'  #dim
        style_pathRight = '\x1b[0m'  #normal
        style_reset     = '\x1b[0m'  #normal
        formatter       = None

        def stylePath(self, path):
            left = self.style_seperator.join(path[:-1])
            right = path[-1:][0]
            return self.style_pathLeft + left + self.style_pathRight + self.style_seperator + right
        
        def styleValue(self, value):
            value = str(value)
            if(value.isnumeric()):
                return self.style_number + value
            return self.style_text + value
        
        def print(self, value, stack, path):
            self._output(self.formatter(self, value, stack, path))
        
        def _output(self, text):
            print(text + self.style_reset)

    # value might be numeric 
    if args.value is not None:
        def detect(v):
            try:
                return int(v)
            except ValueError:
                pass
            try:
                return float(v)
            except ValueError:
                pass
            return v
        types = {
            'int' : int,
            'float' : float,
            'string' : str,
            'auto' : detect
        }
        if args.value.isnumeric():
            search.value = types[args.type](args.value)
        else:
            search.value = args.value
    handlers = {
        'path' : lambda pr, v,s,p : pr.stylePath(p),
        'value' : lambda pr, v,s,p : pr.styleValue(v),
        'both': lambda pr, v,s,p :  "{} : {} ".format(pr.stylePath(p), pr.styleValue(v))
    }    

    x = printer()
    if(args.color == False):
        x.style_text = x.style_number = x.style_pathLeft = x.style_pathRight = x.style_reset

    x.formatter = handlers[args.print]
    search.handler = x.print
    with open(args.file) as file:
        data = file.read()
        file.close()
    data = json.loads(data)
    search.search(data)

