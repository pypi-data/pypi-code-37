# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.190508.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.Devices.Pwm")

try:
    import winrt.windows.devices.pwm.provider
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

class PwmPulsePolarity(enum.IntEnum):
    ACTIVE_HIGH = 0
    ACTIVE_LOW = 1

PwmController = _ns_module.PwmController
PwmPin = _ns_module.PwmPin
