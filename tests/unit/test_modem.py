
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import ubiquiti_monitor.modem as sut


@patch("ubiquiti_monitor.modem.reboot_via_smart_plug")
def test_reboot_works(reboot_mock):
    sut.reboot("asdf")
    assert reboot_mock.called


@patch("ubiquiti_monitor.modem.reboot_via_telnet")
def test_reboot_works_with_telnet(reboot_mock):
    sut.reboot("eth0")
    assert reboot_mock.called


@patch("ubiquiti_monitor.modem.reboot_plug")
@patch("ubiquiti_monitor.modem.find_plug")
def test_reboot_via_smart_plug_works(find_mock, reboot_mock):
    plug = MagicMock()
    plug.on_since = datetime.now() - timedelta(seconds=181)
    find_mock.return_value = plug
    sut.reboot_via_smart_plug("asdf")
    find_mock.assert_called_with("asdf")
    assert reboot_mock.called


@patch("sys.exit")
@patch("ubiquiti_monitor.modem.find_plug")
def test_reboot_via_smart_plug_works_when_plug_not_found(find_mock, exit_mock):
    find_mock.return_value = None
    sut.reboot_via_smart_plug("asdf")
    find_mock.assert_called_with("asdf")
    assert exit_mock.called


def test_should_reboot_plug_works():
    plug = MagicMock()
    plug.on_since = datetime.now() - timedelta(seconds=1)
    assert not sut.should_reboot_plug(plug)


def test_should_reboot_plug_returns_true_when_not_rebooted_in_last_3_minutes():
    plug = MagicMock()
    plug.on_since = datetime.now() - timedelta(seconds=181)
    assert sut.should_reboot_plug(plug)


def test_should_reboot_plug_handles_works_when_on_since_is_None():
    plug = MagicMock()
    plug.on_since = None
    assert sut.should_reboot_plug(plug)


@patch("ubiquiti_monitor.modem.execute_shell")
def test_reboot_via_telnet(exec_mock):
    sut.reboot_via_telnet("eth0")
    exec_mock.assert_called_with(
        f"scripts/uptime.sh 192.168.102.1"
    )


@patch("ubiquiti_monitor.modem.execute_shell")
def test_should_reboot_via_telnet(exec_mock):
    exec_mock.return_value = "181.25"
    result = sut.should_reboot_via_telnet("eth0")
    assert exec_mock.called
    assert result


def test_get_max_time_in_seconds():
    assert sut.get_max_time_in_seconds() == 180
