# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.190508.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.ApplicationModel.Wallet.System")

try:
    import winrt.windows.applicationmodel.wallet
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

class WalletItemAppAssociation(enum.IntEnum):
    NONE = 0
    APP_INSTALLED = 1
    APP_NOT_INSTALLED = 2

WalletItemSystemStore = _ns_module.WalletItemSystemStore
WalletManagerSystem = _ns_module.WalletManagerSystem
