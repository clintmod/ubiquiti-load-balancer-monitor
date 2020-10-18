#!/usr/bin/env python

import logging
import signal
import sys


from time import sleep

from ubiquiti_monitor.modem import reboot
from ubiquiti_monitor.watchdog import get_interface_reports

LOG = logging.getLogger(__name__)

SHOULD_BREAK_LOOP = False


def main():
    try:
        init()
    except KeyboardInterrupt:
        pass


def init():
    init_logging()
    init_signals()
    monitor()


def init_signals():
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)


def signal_handler(signalNumber, frame):
    LOG.info("Exiting because of singal num: %i", signalNumber)
    sys.exit(0)


def init_logging():
    FORMAT = "%(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)s \
%(funcName)s %(message)s"
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=FORMAT)


def monitor():
    LOG.info("Starting monitoring")
    while True:
        reports = get_interface_reports()
        for interface in reports:
            LOG.info(interface.raw_report)
            if interface.is_down():
                LOG.info("Interface %s is down... attempting reboot", interface.name)
                reboot(interface.name)
        sleep(5)
        if SHOULD_BREAK_LOOP:
            break


def module_init(name):
    if name == '__main__':
        main()


module_init(__name__)
