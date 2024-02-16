#!/usr/bin/python

import glob
import time
import sys
import os
import argparse
import logging
from logging.handlers import TimedRotatingFileHandler

def openlog(name):
    logger       = logging.getLogger("Rotating Log")
    logPath      = f"C:/Users/Public/{name}.txt"
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
    name   = "acs_data_search_log"
    logger = openlog(name)

    parser = argparse.ArgumentParser(description="Send metadata to ACS using"
        "Data Search API")

    # Required options needed to push data to ACS
    parser.add_argument("-s", "--source", dest="source", action="store",
        help="ACS Data Source Identifier", required=True)
    parser.add_argument("-i", "--ipname", dest="ipname", action="store",
        help="IP address / hostname and port for ACS server", required=True)
    parser.add_argument("-u", "--user", dest="user", action="store",
        help="username:password", required=True)
    parser.add_argument("-e", "--epoch", dest="epoch", action="store", type=int,
        help="Milliseonds since Epoch", required=True)

    # Additional data left optional with default as empty string
    parser.add_argument("-N", "--name", dest="name", action="store",
        default="", help="Name of the person")
    parser.add_argument("-E", "--extid", dest="extid", action="store",
        default="", help="External Object ID")
    parser.add_argument("-T", "--ptype", dest="ptype", action="store",
        default="", help="Person Type")
    parser.add_argument("-a", "--idclass", dest="idclass", action="store",
        default="", help="ID Class (threat level)")
    parser.add_argument("-m", "--moniker", dest="moniker", action="store",
        default="", help="Moniker")
    parser.add_argument("-D", "--pid", dest="pid", action="store",
        default="", help="Person ID")
    parser.add_argument("-l", "--sim", dest="sim", action="store",
        default="", help="Similarity Score")
    parser.add_argument("-t", "--ptags", dest="ptags", action="store",
        default="", help="Person Tags")


    args = parser.parse_args()

    logger.info(f"Called with arguments: "
        f"source= {args.source} ipname= {args.ipname} "
        f"epoch= {args.epoch} name= {args.name} extid={args.extid} "
        f"ptype= {args.ptype} idclass= {args.idclass} moniker= {args.moniker} "
        f"Person ID= {args.pid} similarity= {args.sim} tags= {args.ptags}")

    # Format time string according to ACS specification.
    milliseconds = args.epoch % 1000
    seconds      = args.epoch / 1000
    t            = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(seconds))
    t           += ".%d" % milliseconds

    logger.info(f"Got time {t}")

    cmd = \
    f"curl --insecure --anyauth -H \"Content-Type: application/json\"" \
    f" --data \"{{ \\\"addExternalDataRequest\\\":" \
    f" {{ \\\"occurrenceTime\\\": \\\"{t}\\\"," \
    f" \\\"source\\\": \\\"{args.source}\\\"," \
    f" \\\"externalDataType\\\": \\\"PointOfSales\\\"," \
    f" \\\"data\\\": {{ \\\"Name\\\": \\\"{args.name}\\\"," \
    f" \\\"Type\\\": \\\"{args.ptype}\\\"," \
    f" \\\"ID Class\\\": \\\"{args.idclass}\\\"," \
    f" \\\"Moniker\\\": \\\"{args.moniker}\\\"," \
    f" \\\"Similarity\\\": \\\"{args.sim}\\\"," \
    f" \\\"Person ID\\\": \\\"{args.pid}\\\"," \
    f" \\\"Tags\\\": \\\"{args.ptags}\\\"," \
    f" \\\"EXT ID\\\": \\\"{args.extid}\\\"}} }} }}\""\
    f" \"https://{args.ipname}/Acs/Api/ExternalDataFacade/AddExternalData\"" \
    f" --user \"{args.user}\""

    #logger.info(cmd)

    ret = os.system(cmd)

    logger.info(ret)


if __name__ == '__main__':
    main()

