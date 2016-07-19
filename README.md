# PyUtils
A small collection of Python utility scripts

File | Description
--- | ---
[crlf](#crlf) | Convert line endings of a file
[ip-ext](#ipext) | Get your external IP address
[jsonsearch](#jsonsearch) | Search through a JSON size

## crlf
Converts the line endings of a file
```sh
$ crlf.py ending input [-o, --output=file] [--overwrite]
```
Argument |  Description | Parameters
--- | --- |---
ending | The line ending to convert to. | { cr, lf, crlf, win, linux, mac }
input |Input file |
-o, --output | Output file |
--overwrite | If output is supplied, overwrite the output. If no output is supplied, overwrite input

Example 1:
```sh
$ crlf.py cr input.txt --overwrite
```
Example 2:
```sh
$ crlf.py cr input.txt -o=output.txt
```

## ip-ext
Prints your external ip address.
```sh
$ ip-ext.py
```
Example output:
```
194.134.26.200
```

## jsonsearch
Search a json file for certain path and/or value.
```sh
$ jsonsearch.py jsonfile [-p, --path=searchpattern] [-v, --value=searchvalue] 
[-l, --limit=displaylimit] [--type=datatype] [--print=format]
```
Argument |  Description | Parameters
--- | --- |---
file | JSON file | 
-p, --path | Partial path of the traversed tree | Text, wildcards allowed
-v, --value | Value to search for | Textual or numeric value
-l, --limit | Limit the number of results |
\-\-type | Datatype of the supplied value | { int, float, string, **auto** }
\-\-output | Output only certain information | { path, value, **both** }
\-\-color | Colors the path and values of output |


Example JSON:
```json
{
   "duration": {
      "value": 300,
      "unit": "minutes"
   },
   "target": {
      "value": 500,
      "unit": "minutes"
   },
   "scores": [
       600,
       500,
       250
   ]
}
```
### Example 1: path
```sh
$ jsonsearch.py test.json -p=*/value
```
```sh
duration/value : 300
target/value : 500
```
### Example 2: value
```sh
$ jsonsearch.py test.json -v=500
```
```
target/value : 500
scores[1] : 500
```

### Example 3: print
```sh
$ jsonsearch.py test.json -v=500 --output=path
```
```
scores[1]
target/value
```