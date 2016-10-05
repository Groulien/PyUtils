#!/usr/bin/env python3
import sys
import json
import fnmatch
import argparse
import platform

class JsonSearch:
    path = None
    value = None
    limit = None
    handler = None
    _count = 0

    def search(self, json):
        self._count = 0
        self._walk(json, [], [])
        return

    def _walk(self, node, stack, path):
        stack.append(node)
        if isinstance(node, dict):
            for n in node:
                value = node[n]
                path.append(n)
                i = len(path)
                self._walk(value, stack, path)
                if i != len(path):
                    print('err')
                    exit(-1)
                path.pop()

        elif isinstance(node, list):
            prefix = path.pop() if len(path) > 0 else ''
            for i in range(0, len(node)):
                value = node[i]
                path.append(prefix+'['+str(i)+']')
                self._walk(value, stack, path)
                path.pop()
            if len(prefix) > 0: 
               path.append(prefix)

        else:
            if self._validate(node, path):
               self.handler(node, stack, path)
               self._count += 1
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
    parser.add_argument('--output', help="output certain data, both by default", choices=['path', 'value', 'both'], default='both')
    parser.add_argument('--color', help="[LINUX ONLY] adds color to printed values", action='store_true', default=False)

    args = parser.parse_args()

    if args.color and platform.system() == 'Windows':
        print('COLORS ARE NOT SUPPORTED ON WINDOWS')
        args.color = False

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
            if len(path) == 1:
                return self.style_pathRight + path[0]
            left = self.style_seperator.join(path[:-1])
            right = path[-1:][0]
            return self.style_pathLeft + left + self.style_pathRight + self.style_seperator + right

        def styleValue(self, value):
            value = str(value)
            if(str(value).isnumeric()):
                return self.style_number + value
            return self.style_text + value

        def output(self, value, stack, path):
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
        args.value = str(args.value) # Windows compatibility
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
        x.style_text = x.style_number = x.style_pathLeft = x.style_pathRight = x.style_reset = ''

    x.formatter = handlers[args.output]
    search.handler = x.output
    with open(args.file) as file:
        data = file.read()
        file.close()
    data = json.loads(data)
    search.search(data)

