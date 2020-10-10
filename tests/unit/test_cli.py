import os

from shutil import copyfile
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

import ubiquiti_monitor.cli as sut


def test_should_reboot_works():
    plug = MagicMock()
    plug.on_since = datetime.now()
    assert sut.should_reboot(plug) == False


def test_should_reboot_returns_true_when_not_already_rebooted():
    plug = MagicMock()
    plug.on_since = datetime.now() - timedelta(seconds=121)
    assert sut.should_reboot(plug)

@patch("ubiquiti_monitor.cli.sleep")
@patch("ubiquiti_monitor.cli.find_plug")
@patch("ubiquiti_monitor.cli.reboot_plug")
@patch("ubiquiti_monitor.models.execute_shell")
def test_main(exec_mock, reboot_mock, find_mock, sleep_mock):
    src = "tests/unit/files/watchdog-down.txt"
    dest = "workdir/watchdog.txt"
    copyfile(src, dest)
    plug = MagicMock()
    plug.on_since = datetime.now() - timedelta(seconds=121)
    find_mock.return_value = plug
    sut.SHOULD_BREAK_LOOP = True
    sut.main()
    assert exec_mock.was_called
    assert reboot_mock.was_called
    assert find_mock.was_called
    assert sleep_mock.was_called_with(5)
    os.remove(dest)


@patch("ubiquiti_monitor.cli.init")
def test_main_handles_KeyboardInterrupt(init_mock):
    init_mock.side_effect = KeyboardInterrupt()
    sut.main()
    assert init_mock.was_called
