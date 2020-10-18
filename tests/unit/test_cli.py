import os

from shutil import copyfile
from unittest.mock import patch

import ubiquiti_monitor.cli as sut


@patch("ubiquiti_monitor.cli.sleep")
@patch("ubiquiti_monitor.cli.reboot")
@patch("ubiquiti_monitor.watchdog.execute_shell")
def test_main(exec_mock, reboot_mock, sleep_mock):
    if not os.path.exists('workdir'):
        os.mkdir('workdir')
    src = "tests/unit/files/watchdog-down.txt"
    dest = "workdir/watchdog.txt"
    copyfile(src, dest)
    sut.SHOULD_BREAK_LOOP = True
    sut.main()
    assert exec_mock.called
    reboot_mock.assert_called_with("eth0")
    sleep_mock.assert_called_with(5)
    os.remove(dest)


@patch("ubiquiti_monitor.cli.init")
def test_main_handles_KeyboardInterrupt(init_mock):
    init_mock.side_effect = KeyboardInterrupt()
    sut.main()
    assert init_mock.called


@patch("sys.exit")
def test_signal_handler(exit_mock):
    sut.signal_handler(0, None)
    assert exit_mock.called


@patch("ubiquiti_monitor.cli.main")
def test_module_init(main_mock):
    sut.module_init("__main__")
    assert main_mock.called
