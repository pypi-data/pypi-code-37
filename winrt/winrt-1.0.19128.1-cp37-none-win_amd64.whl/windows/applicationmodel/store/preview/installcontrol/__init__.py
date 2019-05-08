# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.190508.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.ApplicationModel.Store.Preview.InstallControl")

try:
    import winrt.windows.foundation
except:
    pass

try:
    import winrt.windows.foundation.collections
except:
    pass

try:
    import winrt.windows.management.deployment
except:
    pass

try:
    import winrt.windows.system
except:
    pass

class AppInstallState(enum.IntEnum):
    PENDING = 0
    STARTING = 1
    ACQUIRING_LICENSE = 2
    DOWNLOADING = 3
    RESTORING_DATA = 4
    INSTALLING = 5
    COMPLETED = 6
    CANCELED = 7
    PAUSED = 8
    ERROR = 9
    PAUSED_LOW_BATTERY = 10
    PAUSED_WI_FI_RECOMMENDED = 11
    PAUSED_WI_FI_REQUIRED = 12
    READY_TO_DOWNLOAD = 13

class AppInstallType(enum.IntEnum):
    INSTALL = 0
    UPDATE = 1
    REPAIR = 2

class AppInstallationToastNotificationMode(enum.IntEnum):
    DEFAULT = 0
    TOAST = 1
    TOAST_WITHOUT_POPUP = 2
    NO_TOAST = 3

class AutoUpdateSetting(enum.IntEnum):
    DISABLED = 0
    ENABLED = 1
    DISABLED_BY_POLICY = 2
    ENABLED_BY_POLICY = 3

class GetEntitlementStatus(enum.IntEnum):
    SUCCEEDED = 0
    NO_STORE_ACCOUNT = 1
    NETWORK_ERROR = 2
    SERVER_ERROR = 3

AppInstallItem = _ns_module.AppInstallItem
AppInstallManager = _ns_module.AppInstallManager
AppInstallManagerItemEventArgs = _ns_module.AppInstallManagerItemEventArgs
AppInstallOptions = _ns_module.AppInstallOptions
AppInstallStatus = _ns_module.AppInstallStatus
AppUpdateOptions = _ns_module.AppUpdateOptions
GetEntitlementResult = _ns_module.GetEntitlementResult
