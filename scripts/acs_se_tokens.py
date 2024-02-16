#!/usr/bin/python

import glob
import time
import sys
import os

import argparse
import subprocess
import json

def main():
    parser = argparse.ArgumentParser(description="Send a card number to a"
        " LPR reader in Secure Entry")

    parser.add_argument("-i", "--ipname", dest="ipname", action="store",
        help="IP address / hostname and port for AC unit", required=True)
    parser.add_argument("-x", "--apikey", dest="apikey", action="store",
        help="API Key from Secure Entry", required=True)

    args = parser.parse_args()

    print("********************************")
    print(f"Resource ID Retrieval from IP {args.ipname}")

    cmd = f"curl -s -k --anyauth -H \"X-Api-Key: {args.apikey}\"" \
    f" https://{args.ipname}/nbixagent/resources"

    # Run system command
    output = subprocess.getoutput(cmd)

    try:
        response = json.loads(output)
    except json.decoder.JSONDecodeError:
        print(f"Failed to get tokens:\n {output}")
        sys.exit(1)

    print("***** Access Controller Tokens *******")

    for key, value in response.items():
        for v in value:
            print(f"ID: {v['id']}, Name: {v['name']}, Description:" \
                f" {v['description']}, Door Name: {v['extraInfo']['doorName']}")
    print("***** /Access Controller Tokens *******")

    print("Choose ID token from above and copy in to corresponding ARES" \
    " commandline")

if __name__ == '__main__':
    main()
