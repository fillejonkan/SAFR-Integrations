#!/usr/bin/python

import glob
import time
import sys
import os
import subprocess

import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timezone


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
    name   = "axis_se_log"
    logger = openlog(name)

    parser = argparse.ArgumentParser(description="Send a card number to a"
        "give ID point at a Secure Entry door controller")

    parser.add_argument("-c", "--card", dest="card", action="store",
        help="Card Number to send to access control unit", required=True)
    parser.add_argument("-i", "--ipname", dest="ipname", action="store",
        help="IP address / hostname and port for AC unit", required=True)
    parser.add_argument("-x", "--apikey", dest="apikey", action="store",
        help="API Key from ACS SE", required=True)
    parser.add_argument("-s", "--source", dest="source", action="store",
        help="Resource ID to send read to", required=True)
    parser.set_defaults(tls=False)

    args = parser.parse_args()

    logger.info(f"Called with arguments: "
        f"card = {args.card}, ipname = {args.ipname}, "
        f"source = {args.source}, apikey = {args.apikey}")

    # Ping device to make sure we don't get offline read
    cmd = f"curl -s -k -H \"X-Api-Key: {args.apikey}\"" \
        f" https://{args.ipname}/nbixagent/ping" \
        f" --data \"{{\\\"secondsUntilNextPing\\\": 60," \
        f" \\\"resourceIds\\\": [\\\"{args.source}\\\"]}}\" -i "

    output = subprocess.getoutput(cmd)

    # Check expected return value (204 No data), continue regardless
    if "204" not in output:
        logger.info("Got incorrect return code, check tokens")

    # Get current UTC time on Zulu format needed to send credential
    zulu = datetime.now(timezone.utc).isoformat('T', 'seconds')
    zulu = str(zulu).replace('+00:00', 'Z')

    logger.info(zulu)

    # Send notification / credential to device
    cmd = f"curl -s -k -H \"X-Api-Key: {args.apikey}\"" \
        f" https://{args.ipname}/nbixagent/notifications" \
        f" --data \"{{\\\"items\\\": [{{\\\"dateTime\\\": \\\"{zulu}\\\"," \
        f" \\\"resourceId\\\": \\\"{args.source}\\\", \\\"archetype\\\":" \
        f" \\\"idData\\\", \\\"idData\\\": [{{\\\"type\\\": \\\"vehicleId\\\","\
        f" \\\"plates\\\": [{{\\\"type\\\": \\\"alphanumeric\\\"," \
        f" \\\"id\\\": \\\"{args.card}\\\"}}]}}]}}]}}\" -i"

    output = subprocess.getoutput(cmd)

    # Check expected return value (204 No data), continue regardless
    if "204" not in output:
        logger.info("Got incorrect return code, check tokens")

if __name__ == '__main__':
    main()
