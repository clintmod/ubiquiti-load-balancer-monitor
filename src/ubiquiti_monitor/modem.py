import logging
import sys

from datetime import datetime, timedelta

from ubiquiti_monitor.power_strips import find_plug, reboot_plug
from ubiquiti_monitor.utils import execute_shell

LOG = logging.getLogger(__name__)

THREE_MINS = timedelta(minutes=3)

NAME_IP_MAP = {
    "eth0": "192.168.102.1",
    "eth3": "192.168.100.1"
}


def reboot(name):
    name = name.strip()
    if name in NAME_IP_MAP:
        LOG.info("Rebooting interface %s via telnet", name)
        reboot_via_telnet(name)
    else:
        reboot_via_smart_plug(name)


def reboot_via_smart_plug(name):
    plug = find_plug(name)
    if plug is None:
        LOG.error("plug containing name %s was not found", name)
        sys.exit(1)
        return
    if should_reboot_plug(plug):
        reboot_plug(plug)


def should_reboot_plug(plug):
    current_time = datetime.now()
    if plug.on_since is not None:
        return current_time - THREE_MINS > plug.on_since
    else:
        return True


def reboot_via_telnet(name):
    if should_reboot_via_telnet(name):
        command = f"scripts/reboot_via_telnet.sh {NAME_IP_MAP[name]}"
        execute_shell(command)


def should_reboot_via_telnet(name):
    command = f"scripts/uptime.sh {NAME_IP_MAP[name]}"
    uptime = float(execute_shell(command))
    LOG.info("checking to see if uptime (%s) is greater than %s seconds",
             uptime, get_max_time_in_seconds())
    return uptime > get_max_time_in_seconds()


def get_max_time_in_seconds():
    return THREE_MINS.seconds
