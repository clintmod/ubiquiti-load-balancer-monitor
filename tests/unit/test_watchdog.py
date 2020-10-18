import os

from shutil import copyfile
from unittest.mock import patch

import ubiquiti_monitor.watchdog as sut


@patch('ubiquiti_monitor.watchdog.execute_shell')
def test_get_interface_reports(exec_mock):
    if not os.path.exists('workdir'):
        os.mkdir('workdir')
    src = "tests/unit/files/watchdog.txt"
    dest = "workdir/watchdog.txt"
    copyfile(src, dest)
    sut.get_interface_reports()
    assert exec_mock.called
    os.remove(dest)


@patch('ubiquiti_monitor.watchdog.execute_shell')
def test_create_watchdog_file(exec_mock):
    if os.path.exists('workdir'):
        os.rmdir('workdir')
    sut.create_watchdog_file()
    assert exec_mock.called
    assert os.path.exists('workdir')
