#!/usr/bin/env python3
import subprocess
import re


mac_address = input("Enter the new MAC address (e.g. 00:11:22:33:44:55): ")


if not re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', mac_address):
    print("Invalid MAC address format.")
    exit(1)


subprocess.call("ifconfig eth0 down", shell=True)
subprocess.call(f"ifconfig eth0 hw ether {mac_address}", shell=True)
subprocess.call("ifconfig eth0 up", shell=True)

print(f"MAC address changed to {mac_address}")
