# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.190508.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.Devices.WiFiDirect")

try:
    import winrt.windows.devices.enumeration
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
    import winrt.windows.networking
except:
    pass

try:
    import winrt.windows.security.credentials
except:
    pass

try:
    import winrt.windows.storage.streams
except:
    pass

class WiFiDirectAdvertisementListenStateDiscoverability(enum.IntEnum):
    NONE = 0
    NORMAL = 1
    INTENSIVE = 2

class WiFiDirectAdvertisementPublisherStatus(enum.IntEnum):
    CREATED = 0
    STARTED = 1
    STOPPED = 2
    ABORTED = 3

class WiFiDirectConfigurationMethod(enum.IntEnum):
    PROVIDE_PIN = 0
    DISPLAY_PIN = 1
    PUSH_BUTTON = 2

class WiFiDirectConnectionStatus(enum.IntEnum):
    DISCONNECTED = 0
    CONNECTED = 1

class WiFiDirectDeviceSelectorType(enum.IntEnum):
    DEVICE_INTERFACE = 0
    ASSOCIATION_ENDPOINT = 1

class WiFiDirectError(enum.IntEnum):
    SUCCESS = 0
    RADIO_NOT_AVAILABLE = 1
    RESOURCE_IN_USE = 2

class WiFiDirectPairingProcedure(enum.IntEnum):
    GROUP_OWNER_NEGOTIATION = 0
    INVITATION = 1

WiFiDirectAdvertisement = _ns_module.WiFiDirectAdvertisement
WiFiDirectAdvertisementPublisher = _ns_module.WiFiDirectAdvertisementPublisher
WiFiDirectAdvertisementPublisherStatusChangedEventArgs = _ns_module.WiFiDirectAdvertisementPublisherStatusChangedEventArgs
WiFiDirectConnectionListener = _ns_module.WiFiDirectConnectionListener
WiFiDirectConnectionParameters = _ns_module.WiFiDirectConnectionParameters
WiFiDirectConnectionRequest = _ns_module.WiFiDirectConnectionRequest
WiFiDirectConnectionRequestedEventArgs = _ns_module.WiFiDirectConnectionRequestedEventArgs
WiFiDirectDevice = _ns_module.WiFiDirectDevice
WiFiDirectInformationElement = _ns_module.WiFiDirectInformationElement
WiFiDirectLegacySettings = _ns_module.WiFiDirectLegacySettings
