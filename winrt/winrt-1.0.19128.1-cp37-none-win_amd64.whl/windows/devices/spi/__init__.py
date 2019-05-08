# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.190508.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.Devices.Spi")

try:
    import winrt.windows.devices.spi.provider
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

class SpiMode(enum.IntEnum):
    MODE0 = 0
    MODE1 = 1
    MODE2 = 2
    MODE3 = 3

class SpiSharingMode(enum.IntEnum):
    EXCLUSIVE = 0
    SHARED = 1

SpiBusInfo = _ns_module.SpiBusInfo
SpiConnectionSettings = _ns_module.SpiConnectionSettings
SpiController = _ns_module.SpiController
SpiDevice = _ns_module.SpiDevice
ISpiDeviceStatics = _ns_module.ISpiDeviceStatics
