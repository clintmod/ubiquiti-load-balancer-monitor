#!/usr/bin/env python

import logging
import sys

from datetime import datetime, timedelta
from time import sleep

from ubiquiti_monitor.models import get_interface_reports
from ubiquiti_monitor.power_strips import find_plug, reboot_plug

LOG = logging.getLogger(__name__)

TWO_MINS = timedelta(minutes=2)

SHOULD_BREAK_LOOP = False

def main():
    try:
        init()
    except KeyboardInterrupt:
      pass
    

def init():
    init_logging()
    monitor()


def init_logging():
    FORMAT = "%(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)s %(funcName)s %(message)s"
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=FORMAT)
    

def monitor():
    LOG.info("Starting monitoring")
    while True:
        reports = get_interface_reports()
        for interface in reports:
            LOG.info(interface.raw_report)
            if interface.is_down():
                reboot_modem_plug(interface)
        sleep(5)
        if SHOULD_BREAK_LOOP:
            break


def reboot_modem_plug(interface):
    LOG.info("Interface down %s", interface.raw_report)
    plug = find_plug(interface.name)
    if plug is not None:
        if should_reboot(plug):
            reboot_plug(plug)
    else:
        LOG.error("plug with name %s was not found", interface.name)
        sys.exit(1)



def should_reboot(plug):
    current_time = datetime.now()
    if plug.on_since is not None:
        return current_time - TWO_MINS > plug.on_since
    else:
        return True


if __name__ == '__main__':
    main()
