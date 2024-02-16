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
        "give ID point at an Axis Entry Manager Instance")

    parser.add_argument("-i", "--ipname", dest="ipname", action="store",
        help="IP address / hostname and port for AC unit", required=True)
    parser.add_argument("-u", "--user", dest="user", action="store",
        help="username:password", required=True)
    parser.add_argument('--tls', dest='tls', action='store_true',
        help="Encrypt using TLS")
    parser.add_argument('--no-tls', dest='tls', action='store_false',
        help="Do not encrypt using TLS")
    parser.set_defaults(tls=False)

    args = parser.parse_args()

    print("\n\n\n********************************\n\n\n")
    print(f"Token Retrieval from IP {args.ipname}\n\n\n")

    cmd = f"curl -s --anyauth -H \"Content-Type: application/json\"" \
    f" --data \"{{\\\"pacsaxis:GetAccessControllerList\\\" : {{}}}}\""\
    f" --user \"{args.user}\""

    if args.tls:
        cmd += f" \"https://{args.ipname}/vapix/pacs\" --insecure"
    else:
        cmd += f" \"http://{args.ipname}/vapix/pacs\""

    # Run system command
    output = subprocess.getoutput(cmd)

    try:
        response = json.loads(output)
    except json.decoder.JSONDecodeError:
        print(f"Failed to get tokens:\n {output}")
        sys.exit(1)

    print("***** Access Controller Token *******")

    for key, value in response.items():
        print(f"{key}")
        for v in value:
            print(f"AC Token: {v['token']}, AC Name: {v['Name']}")

    print("***** ID Point Controller Tokens *******")

    cmd = f"curl -s --anyauth -H \"Content-Type: application/json\"" \
    f" --data \"{{\\\"axtid:GetIdPointInfoList\\\" : {{}}}}\""\
    f" --user \"{args.user}\""

    if args.tls:
        cmd += f" \"https://{args.ipname}/vapix/idpoint\" --insecure"
    else:
        cmd += f" \"http://{args.ipname}/vapix/idpoint\""

    output = subprocess.getoutput(cmd)

    try:
        response = json.loads(output)
    except json.decoder.JSONDecodeError:
        print(f"Failed to get tokens:\n {output}")
        sys.exit(1)

    for key, value in response.items():
        print(f"{key}")
        for v in value:
            print(f"IDP Token: {v['token']}, IDP Name: {v['Name']}")

    print("***** Door Tokens *******")

    cmd = f"curl -s --anyauth -H \"Content-Type: application/json\"" \
    f" --data \"{{\\\"tdc:GetDoorInfoList\\\" : {{}}}}\""\
    f" --user \"{args.user}\""

    if args.tls:
        cmd += f" \"https://{args.ipname}/vapix/doorcontrol\" --insecure"
    else:
        cmd += f" \"http://{args.ipname}/vapix/doorcontrol\""

    output = subprocess.getoutput(cmd)

    try:
        response = json.loads(output)
    except json.decoder.JSONDecodeError:
        print(f"Failed to get tokens:\n {output}")
        sys.exit(1)

    for key, value in response.items():
        print(f"{key}")
        for v in value:
            print(f"Door Token: {v['token']}, Door Name: {v['Name']}")



if __name__ == '__main__':
    main()