# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.190508.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.Devices.Input")

try:
    import winrt.windows.foundation
except:
    pass

try:
    import winrt.windows.foundation.collections
except:
    pass

class PointerDeviceType(enum.IntEnum):
    TOUCH = 0
    PEN = 1
    MOUSE = 2

MouseDelta = _ns_module.MouseDelta
PointerDeviceUsage = _ns_module.PointerDeviceUsage
KeyboardCapabilities = _ns_module.KeyboardCapabilities
MouseCapabilities = _ns_module.MouseCapabilities
MouseDevice = _ns_module.MouseDevice
MouseEventArgs = _ns_module.MouseEventArgs
PointerDevice = _ns_module.PointerDevice
TouchCapabilities = _ns_module.TouchCapabilities
