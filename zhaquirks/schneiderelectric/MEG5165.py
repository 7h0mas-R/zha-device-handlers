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
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    WindowCovering.cluster_id,
                    Diagnostic.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Ota.cluster_id,
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
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Diagnostic.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    Ota.cluster_id,
                    WindowCovering.cluster_id,
                ],
            },
        },
    }
    # replacement = {
    #     SKIP_CONFIGURATION: True,
    #     ENDPOINTS: {
    #         1: {
    #             PROFILE_ID: zha.PROFILE_ID,
    #             DEVICE_TYPE: zha.DeviceType.SMART_PLUG,
    #             INPUT_CLUSTERS: [
    #                 BasicCluster,
    #                 PowerConfiguration.cluster_id,
    #                 DeviceTemperature.cluster_id,
    #                 Groups.cluster_id,
    #                 Identify.cluster_id,
    #                 OnOff.cluster_id,
    #                 Scenes.cluster_id,
    #                 BinaryOutput.cluster_id,
    #                 Time.cluster_id,
    #                 ElectricalMeasurementCluster,
    #             ],
    #             OUTPUT_CLUSTERS: [Ota.cluster_id, Time.cluster_id],
    #         },
    #         2: {
    #             PROFILE_ID: zha.PROFILE_ID,
    #             DEVICE_TYPE: zha.DeviceType.MAIN_POWER_OUTLET,
    #             INPUT_CLUSTERS: [AnalogInputCluster],
    #             OUTPUT_CLUSTERS: [AnalogInput.cluster_id, Groups.cluster_id],
    #         },
    #         3: {
    #             PROFILE_ID: zha.PROFILE_ID,
    #             DEVICE_TYPE: zha.DeviceType.METER_INTERFACE,
    #             INPUT_CLUSTERS: [AnalogInput.cluster_id],
    #             OUTPUT_CLUSTERS: [AnalogInput.cluster_id],
    #         },
    #         100: {
    #             PROFILE_ID: zha.PROFILE_ID,
    #             DEVICE_TYPE: zha.DeviceType.OCCUPANCY_SENSOR,
    #             INPUT_CLUSTERS: [BinaryInput.cluster_id],
    #             OUTPUT_CLUSTERS: [BinaryInput.cluster_id, Groups.cluster_id],
    #         },
    #     },
    # }


class SchneiderSettingsCluster(CustomCluster):
    """Schneider Electric Settings Cluster (0xFF17)."""

    name = "Schneider Electric Settings Cluster."
    cluster_id = 0xFF17

    attributes = {
        # Alarm settings
        0x0000: ("led_settings", t.enum8, True),
        0x0001: ("button_mode", t.enum8, True),
        0x0010: ("unknown1", t.uint8_t, True),
        0x0011: ("unknown2", t.uint16_t, True),
        0x0020: ("unknown3", t.uint8_t, True),
        0x0021: ("unknown4", t.uint16_t, True),
        0xFFFD: ("unknown5", t.uint16_t, True),
    }
