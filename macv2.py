#!/usr/bin/env python3
import subprocess
import re
import sys
import tty
import termios


def get_mac_input(prompt="Enter new MAC address: "):
    print(prompt, end="", flush=True)
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        mac = ""
        while True:
            ch = sys.stdin.read(1)
            if ch in ['\r', '\n']:
                print()  # Newline after Enter
                break
            elif ch == '\x7f':  # Backspace
                if len(mac) > 0:
                    mac = mac[:-1]
                    print('\b \b', end="", flush=True)
                    if len(mac.replace(":", "")) % 2 == 0 and mac.endswith(":"):
                        mac = mac[:-1]
                        print('\b \b', end="", flush=True)
            elif ch.lower() in "0123456789abcdef":
                if len(mac.replace(":", "")) < 12:
                    mac += ch
                    print(ch, end="", flush=True)
                    if len(mac.replace(":", "")) % 2 == 0 and len(mac.replace(":", "")) < 12:
                        mac += ":"
                        print(":", end="", flush=True)
            # Ignore other keys
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return mac


def run_command(command):
    subprocess.call(command, shell=True)


mac_address = get_mac_input("Enter the new MAC address (auto-colon): ")

# Validate MAC
if not re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', mac_address):
    print("❌ Invalid MAC address format.")
    exit(1)

# Change MAC address
run_command("ifconfig eth0 down")
run_command(f"ifconfig eth0 hw ether {mac_address}")
run_command("ifconfig eth0 up")

print(f"✅ MAC address changed to {mac_address}")
