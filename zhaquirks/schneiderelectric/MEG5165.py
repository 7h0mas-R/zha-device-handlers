"""Merten MEG5165 PlusLink Shutter insert with Merten Wiser System M Push Button (1fold)."""
from zigpy.profiles import zha
from zigpy.quirks import CustomCluster, CustomDevice
import zigpy.types as t
from zigpy.zcl.clusters.closures import WindowCovering
from zigpy.zcl.clusters.general import (
    Basic,
    Groups,
    Identify,
    LevelControl,
    OnOff,
    Ota,
    Scenes,
)
from zigpy.zcl.clusters.homeautomation import Diagnostic

from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)

ATTR_CURRENT_POSITION_LIFT_PERCENTAGE = 0x0008
CMD_GO_TO_LIFT_PERCENTAGE = 0x0005


class SchneiderWindowCovering(CustomCluster, WindowCovering):
    """Schneider Electric Window covering cluster."""

    def _update_attribute(self, attrid, value):
        if attrid == ATTR_CURRENT_POSITION_LIFT_PERCENTAGE:
            # Invert the percentage value (cf https://github.com/dresden-elektronik/deconz-rest-plugin/issues/3757)
            value = 100 - value
        super()._update_attribute(attrid, value)

    async def command(
        self, command_id, *args, manufacturer=None, expect_reply=True, tsn=None
    ):
        """Override default command to invert percent lift value."""
        if command_id == CMD_GO_TO_LIFT_PERCENTAGE:
            percent = args[0]
            # Invert the percentage value
            percent = 100 - percent
            v = (percent,)
            return await super().command(command_id, *v)
        return await super().command(
            command_id,
            *args,
            manufacturer=manufacturer,
            expect_reply=expect_reply,
            tsn=tsn,
        )


class SchneiderElectricCustomCluster(CustomCluster):
    """Schneider Electric Settings Cluster (0xFF17)."""

    name = "Schneider Electric Settings Cluster."
    cluster_id = 0xFF17

    attributes = CustomCluster.attributes.copy()
    attributes.update(
        {
            # Alarm settings
            0x0000: ("led_settings", t.enum8, 0),
            0x0001: ("button_mode", t.enum8, 3),
            0x0010: ("unknown1", t.uint8_t, 0),
            0x0011: ("unknown2", t.uint16_t, 0),
            0x0020: ("unknown3", t.uint8_t, 1),
            0x0021: ("unknown4", t.uint16_t, 0),
            0xFFFD: ("unknown5", t.uint16_t, 1),
        }
    )


class WiserShutterInsertMEG5165(CustomDevice):
    """1GANG/SHUTTER/1"""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)

    signature = {
        MODELS_INFO: [("Schneider Electric", "1GANG/SHUTTER/1")],
        ENDPOINTS: {
            # <SimpleDescriptor endpoint=5 profile=260 device_type=514
            # device_version=0
            # input_clusters=[0, 3, 4, 5, 258, 2821]
            # output_clusters=[25]>
            5: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.WINDOW_COVERING_DEVICE,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,  # 0x0000
                    Identify.cluster_id,  # 0x0003
                    Groups.cluster_id,  # 0x0004
                    Scenes.cluster_id,  # 0x0005
                    WindowCovering.cluster_id,  # 0x0102
                    Diagnostic.cluster_id,  # 0x0b05
                ],
                OUTPUT_CLUSTERS: [
                    Ota.cluster_id,  # 0x0019
                ],
            },
            # <SimpleDescriptor endpoint=21 profile=260 device_type=260
            # device_version=0
            # input_clusters=[0, 3, 2821, 65303]
            # output_clusters=[3, 5, 6, 8, 25, 258]>
            21: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.DIMMER_SWITCH,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,  # 0x0000
                    Identify.cluster_id,  # 0x0003
                    Diagnostic.cluster_id,  # 0x0b05
                    0xFF17,  # Schneider specific settings
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,  # 0x0003
                    Scenes.cluster_id,  # 0x0005
                    OnOff.cluster_id,  # 0x0006
                    LevelControl.cluster_id,  # 0x0008
                    Ota.cluster_id,  # 0x0019
                    WindowCovering.cluster_id,  # 0x0102
                ],
            },
        },
    }
    replacement = {
        ENDPOINTS: {
            5: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.WINDOW_COVERING_DEVICE,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,  # 0x0000
                    Identify.cluster_id,  # 0x0003
                    Groups.cluster_id,  # 0x0004
                    Scenes.cluster_id,  # 0x0005
                    SchneiderWindowCovering,  # invert position
                    Diagnostic.cluster_id,  # 0x0b05
                ],
                OUTPUT_CLUSTERS: [
                    Ota.cluster_id,  # 0x0019
                ],
            },
            21: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.DIMMER_SWITCH,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,  # 0x0000
                    Identify.cluster_id,  # 0x0003
                    Diagnostic.cluster_id,  # 0x0b05
                    SchneiderElectricCustomCluster,  # Schneider specific settings
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,  # 0x0003
                    Scenes.cluster_id,  # 0x0005
                    OnOff.cluster_id,  # 0x0006
                    LevelControl.cluster_id,  # 0x0008
                    Ota.cluster_id,  # 0x0019
                    WindowCovering.cluster_id,  # 0x0102
                ],
            },
        },
    }
