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
    name   = "acs_trigger_log"
    logger = openlog(name)

    parser = argparse.ArgumentParser(description="Send a trigger with a given"
        "name to a given ACS instance")

    parser.add_argument("-t", "--trigger", dest="trigger", action="store",
        help="name of the ACS trigger", required=True)
    parser.add_argument("-i", "--ipname", dest="ipname", action="store",
        help="IP address / hostname and port for ACS server", required=True)
    parser.add_argument("-u", "--user", dest="user", action="store",
        help="username:password", required=True)

    args = parser.parse_args()

    logger.info(f"Called with arguments: "
        f"trigger= {args.trigger} ipname= {args.ipname}")

    # Build cURL command from arguments
    cmd = f"curl --insecure --anyauth -g " \
    f"\"https://{args.ipname}/Acs/Api/TriggerFacade/ActivateDeactivateTrigger?"\
    f"{{\\\"triggerName\\\":\\\"{args.trigger}\\\"," \
    f"\\\"deactivateAfterSeconds\\\":\\\"5\\\"}}\"" \
    f" --user \"{args.user}\""

    #logger.info(cmd)

    # Run system command
    os.system(cmd)

if __name__ == '__main__':
    main()


