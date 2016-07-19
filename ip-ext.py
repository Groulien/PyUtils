#!/usr/bin/env python3
# Gets the external IP address
from urllib.request import urlopen
def extIp():
    source = 'http://icanhazip.com'
    ip = 'Unknown'
    ip = urlopen(source).read().decode('ascii').rstrip()
    return ip
if __name__ == "__main__":
    print(extIp())
