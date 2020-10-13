import logging
import os

from ubiquiti_monitor.utils import execute_shell

LOG = logging.getLogger(__name__)

class InterfaceReport:
    def __init__(self, report):
        self.raw_report = report
        self.name = report.get("name")
        self.pings = report.get("pings")
        self.fails = report.get("fails")
        self.run_fails = report.get("run fails")
        self.route_drops = report.get("route drops")
        self.ping_gateway = report.get("ping gateway")
        self.last_route_drop = report.get("last route drop")
        self.last_route_recover = report.get("last route recover")


    def is_down(self):
        if self.ping_gateway is not None and "DOWN" in self.ping_gateway:
            return True
        else:
            return False


def get_interface_reports():
    return_value = []
    create_watchdog_file()
    contents = get_watchdog_contents_as_array()
    reports = parse_contents(contents)
    for eth_name in reports:
        report = reports[eth_name]
        return_value.append(InterfaceReport(report))
    return return_value


def create_watchdog_file():
    if not os.path.exists('workdir'):
        os.mkdir('workdir')
    command = "mkdir -p ~/.ssh && \
ssh-keyscan -H 192.168.10.1 >> ~/.ssh/known_hosts && \
sshpass -e ssh -q clint@192.168.10.1 /opt/vyatta/bin/vyatta-op-cmd-wrapper \
show load-balance watchdog > workdir/watchdog.txt"
    execute_shell(command)


def get_watchdog_contents_as_array():
    with open('workdir/watchdog.txt') as file:
        return file.readlines()[1:-2] # throw away the first line and the last 3 lines


def parse_contents(contents):
    return_value = {}
    joined = "".join(contents)
    parts = joined.split("\n\n")
    parts = [x.strip() for x in parts]
    LOG.debug("parts = %s", parts)
    for part in parts:
        eth_name, report = parse_part(part)
        return_value[eth_name] = report
    return return_value


def parse_part(part):
    LOG.debug("part = %s", part)
    return_value = {}
    lines = part.split("\n")
    lines = [x.strip() for x in lines]
    eth = lines.pop(0)
    return_value["name"] = eth
    for line in lines:
        line_part = line.split(": ")
        LOG.debug("line_part = %s", line_part)
        return_value[line_part[0].strip()] = line_part[1].strip()
    return return_value["name"], return_value
