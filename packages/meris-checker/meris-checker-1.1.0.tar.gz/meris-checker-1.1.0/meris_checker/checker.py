#!/usr/bin/env python3

import sys
import time
import json
import ipaddress
from os.path import exists
from urllib.request import urlopen


def main():
    ips_txt_lines = [] if not exists("ips.txt") else list(open("ips.txt"))

    lines = sys.argv[1:] + ips_txt_lines

    for line in lines:
        net = ipaddress.ip_network(line.strip())
        for ip in net:
            response = urlopen(f"https://radar.qrator.net/blog/meris-check?ip={ip}")
            payload = json.load(response)
            if payload["affected"]:
                print(f"IP {ip} is affected by Meris!!!!")
            else:
                print(f"IP {ip} is safe, whew!")
            time.sleep(1)


if __name__ == "__main__":
    main()
