import asyncio
import logging


from time import sleep
from kasa import SmartStrip

LOG = logging.getLogger(__name__)

STRIPS = [SmartStrip("192.168.0.123"), SmartStrip("192.168.0.194")]


def reboot_plug(plug):
    LOG.info("rebooting plug %s", plug.alias)
    asyncio.run(plug.turn_off())
    sleep(3)
    asyncio.run(plug.turn_on())


def find_plug(plug_name):
    return_value = None
    for strip in STRIPS:
        asyncio.run(strip.update())
        for plug in strip.children:
            if plug_name in plug.alias:
                return_value = plug
    return return_value
