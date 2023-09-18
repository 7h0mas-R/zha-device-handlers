"""Tests for Schneider Electric Merten Wiser Shutter Insert."""
from unittest import mock

import pytest
from zigpy.zcl.clusters.closures import WindowCovering

from zhaquirks.schneiderelectric.MEG5165 import WiserShutterInsertMEG5165

from tests.common import ClusterListener


@pytest.mark.parametrize("quirk", (WiserShutterInsertMEG5165,))
async def test_WiserShutter(zigpy_device_from_quirk, quirk):
    """Test Wiser Shutter insert."""

    device = zigpy_device_from_quirk(quirk)
    device.request = mock.AsyncMock()

    covering_cluster = device.endpoints[5].window_covering
    schneider_cluster = device.endpoints[21].SchneiderSettingsCluster
    schneider_listener = ClusterListener(schneider_cluster)

    # dev_led_settings_attr_id = schneider_cluster.attributes_by_name["led_settings"].id

    # schneider_cluster._update_attribute(dev_led_settings_attr_id,3)
    # assert len(dev_schneider_listener.attribute_updates) == 1
    # assert dev_schneider_listener.attribute_updates[0][0] == dev_led_settings_attr_id

    """Test that the Smartwings WM25/L-Z blind quirk inverts the up/down commands"""
    close_command_id = WindowCovering.commands_by_name["down_close"].id
    open_command_id = WindowCovering.commands_by_name["up_open"].id
    go_to_command_id = WindowCovering.commands_by_name["go_to_lift_percentage"].id

    # close cover
    await covering_cluster.command(close_command_id)
    assert len(device.request.mock_calls) == 1
    # (260, 258, 5, 5, 1, b'\x01\x01\x01')
    # 01 close/down
    assert device.request.mock_calls[0][1][5] == b"\x01\x01\x01"

    # open cover
    await covering_cluster.command(open_command_id)
    assert len(device.request.mock_calls) == 2
    # (260, 258, 5, 5, 2, b'\x01\x02\x00')
    # 00: open/up
    assert device.request.mock_calls[1][1][5] == b"\x01\x02\x00"

    # move to position must invert position
    await covering_cluster.command(go_to_command_id, 95)
    assert len(device.request.mock_calls) == 3
    # (profile_id,cluster,self._endpoint_id,self._endpoint_id,sequence,data,expect_reply=expect_reply,d)
    # (260, 258, 5, 5, 3, b'\x01\x03\x05\x05')
    # 05: goto lift percentage, 05 percentage
    assert device.request.mock_calls[2][1][5] == b"\x01\x03\x05\x05"

    await covering_cluster.command(go_to_command_id, 10)
    assert len(device.request.mock_calls) == 4
    # (260, 258, 5, 5, 4, b'\x01\x04\x05Z')
    # 05: go to lift percentage, x5A=90 percentage
    assert device.request.mock_calls[3][1][5] == b"\x01\x04\x05\x5A"

    """Test some stuff on the Schneider Settings Cluster"""
    schneider_cluster._update_attribute(0x0000, 0)
    assert schneider_listener.attribute_updates[0][0] == 0
    assert schneider_listener.attribute_updates[0][1] == 0

    schneider_cluster._update_attribute(0x0000, 1)
    assert schneider_listener.attribute_updates[1][0] == 0
    assert schneider_listener.attribute_updates[1][1] == 1
