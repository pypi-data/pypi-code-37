# WARNING: Please don't edit this file. It was generated by Python/WinRT v0.9.190508.1

import typing, winrt
import enum

_ns_module = winrt._import_ns_module("Windows.Media.Render")

class AudioRenderCategory(enum.IntEnum):
    OTHER = 0
    FOREGROUND_ONLY_MEDIA = 1
    BACKGROUND_CAPABLE_MEDIA = 2
    COMMUNICATIONS = 3
    ALERTS = 4
    SOUND_EFFECTS = 5
    GAME_EFFECTS = 6
    GAME_MEDIA = 7
    GAME_CHAT = 8
    SPEECH = 9
    MOVIE = 10
    MEDIA = 11

