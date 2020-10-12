import os

from shutil import copyfile
from unittest.mock import MagicMock, patch

import ubiquiti_monitor.models as sut


@patch('ubiquiti_monitor.models.execute_shell')
def test_get_interface_reports(exec_mock):
    if not os.path.exists('workdir'):
        os.mkdir('workdir')
    src = "tests/unit/files/watchdog.txt"
    dest = "workdir/watchdog.txt"
    copyfile(src, dest)
    sut.get_interface_reports()
    assert exec_mock.was_called
    os.remove(dest)
