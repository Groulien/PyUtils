#!/usr/bin/env python3
# Gets the external IP address
from urllib.request import urlopen
source = "http://icanhazip.com/"
ip = "Unknown"
ip = urlopen(source).read().decode("ascii").rstrip()
print(ip);