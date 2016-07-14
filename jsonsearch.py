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
        self._walk(json, [json], '')
        return

    def _walk(self, node, stack, path):
        for n in node:
            if(self._count == self.limit):
                return
            value = node[n]
            stack.append(value)
            if isinstance(value, dict):
                self._walk(value, stack, path+'/'+n)
            elif isinstance(value, list):
                for i in range(0,len(value)):
                    if(self._count == self.limit):
                        return
                    self._walk(value[i], stack, path+'/'+n+'['+str(i)+']')
            else:
                if(self._validate(value, path+'/'+n)):
                    self.handler(value, stack, path+'/'+n)
                    self._count += 1
            stack.pop()

    def _validate(self, value, path):
        return (self.path == None or fnmatch.fnmatch(path, self.path)) and (self.value == None or self.value == value)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search JSON in path or for values. Author: By Niek Hoekstra',)
    parser.add_argument('file', help='JSON file')

    parser.add_argument('-p', '--path', help='Search in JSON path, wildcards allowed. Example: */duration/value', default=None)
    parser.add_argument('-v', '--value', help='Search for value', default=None)
    parser.add_argument('-l', '--limit',  help='Limit the number of results', type=int, default=None)
    parser.add_argument('--type', help='Forces datatype for the value', choices=['int', 'float', 'string', 'auto'], default='auto')
    parser.add_argument('--print', help="print certain data, both by default", choices=['path', 'value', 'both'], default='both')

    args = parser.parse_args()

    if(args.path == None and args.value == None):
        print('Must search path and/or value.')
        exit(-1)

    search = JsonSearch()
    search.path = args.path
    search.value = args.value
    search.limit = args.limit
    # value might be numeric 
    if(args.value is not None):
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
        search.value = types[args.type](args.value)

    handlers = {
        'path' : lambda v,s,p : print(p),
        'value' : lambda v,s,p : print(str(v)),
        'both': lambda v,s,p : print(p+' : '+str(v))
    }
    search.handler = handlers[args.print]
    with open(args.file) as file:
        data = file.read()
        file.close()
    data = json.loads(data)
    search.search(data)

