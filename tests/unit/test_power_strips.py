from unittest.mock import MagicMock, patch

import ubiquiti_monitor.power_strips as sut

@patch("ubiquiti_monitor.power_strips.sleep")
@patch("asyncio.run")
def test_reboot_plug(mock_run, mock_sleep):
    plug = MagicMock()
    sut.reboot_plug(plug)
    assert mock_run.was_called
    assert mock_sleep.was_called_with(3)
    assert plug.turn_off.was_called
    assert plug.turn_on.was_called


@patch("asyncio.run")
def test_find_plug(mock_run):
    mock_strip_1 = MagicMock()
    mock_strip_2 = MagicMock()
    mock_plug = MagicMock()
    mock_plug.alias = "a long name with asdf in it"
    mock_strip_2.children = [mock_plug]
    strips = [mock_strip_1, mock_strip_2]
    sut.STRIPS = strips
    found_plug = sut.find_plug("asdf")
    assert mock_run.was_called
    assert found_plug == mock_plug
