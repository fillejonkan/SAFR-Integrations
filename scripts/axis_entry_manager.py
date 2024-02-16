#!/usr/bin/python

import glob
import time
import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler

import argparse

def openlog(name):
    logger = logging.getLogger("Rotating Log")
    logPath = f"C:/Users/Public/{name}.txt"
    logFormatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s]' \
        '[%(levelname)-5.5s] %(message)s')
    # configure file logging
    fileHandler = TimedRotatingFileHandler(logPath, when="d", interval=1,
        backupCount=14)
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)
    # configure console logging
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)
    # set logging level
    logger.setLevel(logging.INFO)

    return logger

def main():
    name   = "axis_entry_manager_log"
    logger = openlog(name)

    parser = argparse.ArgumentParser(description="Send a card number to a"
        "give ID point at an Axis Entry Manager Instance")

    parser.add_argument("-c", "--card", dest="card", action="store", type=int,
        help="Card Number to send to access control unit", required=True)
    parser.add_argument("-i", "--ipname", dest="ipname", action="store",
        help="IP address / hostname and port for AC unit", required=True)
    parser.add_argument("-u", "--user", dest="user", action="store",
        help="username:password", required=True)
    parser.add_argument("-s", "--source", dest="source", action="store",
        help="Source Token (ID Point token)", required=True)
    parser.add_argument("-t", "--target", dest="target", action="store",
        help="Target Token (Door token)", required=False, default="")
    parser.add_argument("-a", "--ac", dest="ac", action="store",
        help="Access Controller Token", required=True)
    parser.add_argument('--tls', dest='tls', action='store_true',
        help="Encrypt using TLS")
    parser.add_argument('--no-tls', dest='tls', action='store_false',
        help="Do not encrypt using TLS")
    parser.set_defaults(tls=False)

    args = parser.parse_args()

    logger.info(f"Called with arguments: "
        f"card = {args.card}, ipname = {args.ipname}, "
        f"source = {args.source}, target = {args.target}, ac = {args.ac},"
        f" tls = {args.tls}")

    cmd = f"curl --anyauth -H \"Content-Type: application/json\"" \
    f" --data \"{{\\\"pacsaxis:RequestAccess\\\" : {{\\\"Action\\\" :" \
    f" \\\"Access\\\",\\\"IdData\\\" : " \
    f"[ {{\\\"Name\\\" : \\\"CardNr\\\",\\\"Value\\\": \\\"{args.card}\\\"}}],"\
    f" \\\"SourceToken\\\" : \\\"{args.source}\\\","\
    f" \\\"TargetToken\\\" : \\\"{args.target}\\\","\
    f" \\\"Token\\\" : \\\"{args.ac}\\\"}}}}\"" \
    f" --user \"{args.user}\" "

    if args.tls:
        cmd += f"\"https://{args.ipname}/vapix/pacs\" --insecure"
    else:
        cmd += f"\"http://{args.ipname}/vapix/pacs\""

    #logger.info(cmd)

    # Run system command
    os.system(cmd)

if __name__ == '__main__':
    main()