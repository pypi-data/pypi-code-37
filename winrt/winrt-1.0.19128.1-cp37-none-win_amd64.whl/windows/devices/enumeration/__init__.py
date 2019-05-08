# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.190508.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.Devices.Enumeration")

try:
    import winrt.windows.applicationmodel.background
except:
    pass

try:
    import winrt.windows.foundation
except:
    pass

try:
    import winrt.windows.foundation.collections
except:
    pass

try:
    import winrt.windows.storage.streams
except:
    pass

try:
    import winrt.windows.ui
except:
    pass

try:
    import winrt.windows.ui.popups
except:
    pass

class DeviceAccessStatus(enum.IntEnum):
    UNSPECIFIED = 0
    ALLOWED = 1
    DENIED_BY_USER = 2
    DENIED_BY_SYSTEM = 3

class DeviceClass(enum.IntEnum):
    ALL = 0
    AUDIO_CAPTURE = 1
    AUDIO_RENDER = 2
    PORTABLE_STORAGE_DEVICE = 3
    VIDEO_CAPTURE = 4
    IMAGE_SCANNER = 5
    LOCATION = 6

class DeviceInformationKind(enum.IntEnum):
    UNKNOWN = 0
    DEVICE_INTERFACE = 1
    DEVICE_CONTAINER = 2
    DEVICE = 3
    DEVICE_INTERFACE_CLASS = 4
    ASSOCIATION_ENDPOINT = 5
    ASSOCIATION_ENDPOINT_CONTAINER = 6
    ASSOCIATION_ENDPOINT_SERVICE = 7
    DEVICE_PANEL = 8

class DevicePairingKinds(enum.IntFlag):
    NONE = 0
    CONFIRM_ONLY = 0x1
    DISPLAY_PIN = 0x2
    PROVIDE_PIN = 0x4
    CONFIRM_PIN_MATCH = 0x8

class DevicePairingProtectionLevel(enum.IntEnum):
    DEFAULT = 0
    NONE = 1
    ENCRYPTION = 2
    ENCRYPTION_AND_AUTHENTICATION = 3

class DevicePairingResultStatus(enum.IntEnum):
    PAIRED = 0
    NOT_READY_TO_PAIR = 1
    NOT_PAIRED = 2
    ALREADY_PAIRED = 3
    CONNECTION_REJECTED = 4
    TOO_MANY_CONNECTIONS = 5
    HARDWARE_FAILURE = 6
    AUTHENTICATION_TIMEOUT = 7
    AUTHENTICATION_NOT_ALLOWED = 8
    AUTHENTICATION_FAILURE = 9
    NO_SUPPORTED_PROFILES = 10
    PROTECTION_LEVEL_COULD_NOT_BE_MET = 11
    ACCESS_DENIED = 12
    INVALID_CEREMONY_DATA = 13
    PAIRING_CANCELED = 14
    OPERATION_ALREADY_IN_PROGRESS = 15
    REQUIRED_HANDLER_NOT_REGISTERED = 16
    REJECTED_BY_HANDLER = 17
    REMOTE_DEVICE_HAS_ASSOCIATION = 18
    FAILED = 19

class DevicePickerDisplayStatusOptions(enum.IntFlag):
    NONE = 0
    SHOW_PROGRESS = 0x1
    SHOW_DISCONNECT_BUTTON = 0x2
    SHOW_RETRY_BUTTON = 0x4

class DeviceUnpairingResultStatus(enum.IntEnum):
    UNPAIRED = 0
    ALREADY_UNPAIRED = 1
    OPERATION_ALREADY_IN_PROGRESS = 2
    ACCESS_DENIED = 3
    FAILED = 4

class DeviceWatcherEventKind(enum.IntEnum):
    ADD = 0
    UPDATE = 1
    REMOVE = 2

class DeviceWatcherStatus(enum.IntEnum):
    CREATED = 0
    STARTED = 1
    ENUMERATION_COMPLETED = 2
    STOPPING = 3
    STOPPED = 4
    ABORTED = 5

class Panel(enum.IntEnum):
    UNKNOWN = 0
    FRONT = 1
    BACK = 2
    TOP = 3
    BOTTOM = 4
    LEFT = 5
    RIGHT = 6

DeviceAccessChangedEventArgs = _ns_module.DeviceAccessChangedEventArgs
DeviceAccessInformation = _ns_module.DeviceAccessInformation
DeviceConnectionChangeTriggerDetails = _ns_module.DeviceConnectionChangeTriggerDetails
DeviceDisconnectButtonClickedEventArgs = _ns_module.DeviceDisconnectButtonClickedEventArgs
DeviceInformation = _ns_module.DeviceInformation
DeviceInformationCollection = _ns_module.DeviceInformationCollection
DeviceInformationCustomPairing = _ns_module.DeviceInformationCustomPairing
DeviceInformationPairing = _ns_module.DeviceInformationPairing
DeviceInformationUpdate = _ns_module.DeviceInformationUpdate
DevicePairingRequestedEventArgs = _ns_module.DevicePairingRequestedEventArgs
DevicePairingResult = _ns_module.DevicePairingResult
DevicePicker = _ns_module.DevicePicker
DevicePickerAppearance = _ns_module.DevicePickerAppearance
DevicePickerFilter = _ns_module.DevicePickerFilter
DeviceSelectedEventArgs = _ns_module.DeviceSelectedEventArgs
DeviceThumbnail = _ns_module.DeviceThumbnail
DeviceUnpairingResult = _ns_module.DeviceUnpairingResult
DeviceWatcher = _ns_module.DeviceWatcher
DeviceWatcherEvent = _ns_module.DeviceWatcherEvent
DeviceWatcherTriggerDetails = _ns_module.DeviceWatcherTriggerDetails
EnclosureLocation = _ns_module.EnclosureLocation
IDevicePairingSettings = _ns_module.IDevicePairingSettings
