import re
from enti.api.processor import *

def _cased(l):
    cased_l = []
    for lower, value in l:
        cased_l.append(
            (
                lower,
                re.compile(r"\b({}|{}|{})\b"
                           .format(lower,lower.upper(),
                                   lower.title())),
                value
            )
        )
    return cased_l


COUPLE = 2
#FEW = (3, 5)
#SEVERAL = (4, 8)
DOZEN = 12


UNITS = _cased([
    ('zero', 0),
    ('one', 1),
    ('two', 2),
    ('three', 3),
    ('four', 4),
    ('five', 5),
    ('six', 6),
    ('seven', 7),
    ('eight', 8),
    ('nine', 9),
    ('ten', 10),
    ('eleven', 11),
    ('twelve', 12),
    ('thirteen', 13),
    ('fourteen', 14),
    ('fifteen', 15),
    ('sixteen', 16),
    ('seventeen', 17),
    ('eighteen', 18),
    ('nineteen', 19),
])
UNITS.reverse()

TENS = _cased([
    ('ten', 10),
    ('twenty', 20),
    ('thirty', 30),
    ('forty', 40),
    ('fifty', 50),
    ('sixty', 60),
    ('seventy', 70),
    ('eighty', 80),
    ('ninety', 90),
])

SCALES = _cased([
    ("dozen", 12),
    ("hundred", 10 ** 2),
    ("thousand", 10 ** 3),
    ("million", 10 ** 6),
    ("billion", 10 ** 9),
    ("trillion", 10 ** 12),
])

_enc_unit = lambda x: f"<Q:U>{x}</Q:U>"
_enc_ten = lambda x: f"<Q:T>{x}</Q:T>"
_enc_scale = lambda x: f"<Q:S>{x}</Q:S>"

_U_CONCAT_T = ("u-concat-t",
               re.compile(r"<Q:U>([0-9]+)</Q:U>[ -]?(?:and)? ?<Q:T>([0-9]+)</Q:T>"),
               lambda m: f"<Q:U>{int(m.group(1))}{int(m.group(2))}</Q:U>"
               )
_T_CONCAT_T = ("t-concat-t",
               re.compile(r"<Q:T>([0-9]+)</Q:T>[ \-]?(?:and)? ?<Q:T>([0-9]+)</Q:T>"),
               lambda m: f"<Q:U>{int(m.group(1))}{int(m.group(2))}</Q:U>"
               )
_T_ADD_U = ("t-add-u",
            re.compile(r"<Q:T>([0-9]+)</Q:T>[ \-]?<Q:U>([0-9]+)</Q:U>"),
            lambda m: f"<Q:U>{int(m.group(1)) + int(m.group(2))}</Q:U>"
            )
_U_MULT_S = ("u-mult-s",
             re.compile(r"<Q:U>([0-9]+)</Q:U>[ \-]?<Q:S>([0-9]+)</Q:S>"),
             lambda m: f"<Q:R>{int(m.group(1)) * int(m.group(2))}</Q:R>"
             )
_U_TO_R = ("u-to-r",
           re.compile(r"<Q:U>([0-9]+)</Q:U>"),
           lambda m: f"<Q:R>{int(m.group(1))}</Q:R>"
           )
_R_MULT_S = ("r-mult-s",
             re.compile(r"<Q:R>([0-9]+)</Q:R>[ \-]?<Q:S>([0-9]+)</Q:S>"),
             lambda m: f"<Q:R>{int(m.group(1)) * int(m.group(2))}</Q:R>"
             )
_R_ADD_R = ("r-add-r",
            re.compile(f"<Q:R>([0-9]+)</Q:R> ?(?:[ \-,]| and ) ?<Q:R>([0-9]+)</Q:R>"),
            lambda m: f"<Q:R>{int(m.group(1)) + int(m.group(2))}</Q:R>"
            )
_R_ADD_U = ("r-add-u",
            re.compile(r"<Q:R>([0-9]+)</Q:R>[ \-]?<Q:U>([0-9]+)</Q:U>"),
            lambda m: f"<Q:R>{int(m.group(1)) + int(m.group(2))}</Q:R>"
            )
_S_ADD_R = ("s-add-r",
            re.compile(f"<Q:S>([0-9]+)</Q:S> ?(?:[ \-,]| and ) ?<Q:R>([0-9]+)</Q:R>"),
            lambda m: f"<Q:R>{int(m.group(1)) + int(m.group(2))}</Q:R>"
            )
_R_FINAL = ("r-final",
            re.compile(r"<Q:R>([0-9]+)</Q:R>"),
            r"<Q:F>\1</Q:F>"
            )
_S_FINAL = ("s-final",
            re.compile(r"<Q:S>([0-9]+)</Q:S>"),
            r"<Q:F>\1</Q:F>"
            )
_U_FINAL = ("u-final",
            re.compile(r"<Q:U>([0-9]+)</Q:U>"),
            r"<Q:F>\1</Q:F>"
            )
_T_FINAL = ("t-final",
            re.compile(r"<Q:T>([0-9]+)</Q:T>"),
            r"<Q:F>\1</Q:F>"
            )

# _FEW_SPLIT_F = ("few-split-f",
#                 re.compile(r"[Aa]? few <Q:F>([0-9]+)</Q:F>"),
#                 lambda m: f"<Q:F>{FEW[0] * int(m.group(1))}</Q:F> to <Q:F>{FEW[1] * int(m.group(1))}</Q:F>"
#                 )
_COUPLE_F = ("couple-f",
             re.compile(r"[Aa]? couple <Q:F>([0-9]+)</Q:F>(?: of)?"),
             lambda m: f"<Q:F>{COUPLE * int(m.group(1))}</Q:F>"
             )
# _SEVERAL_SPLIT_F = ("several-split-f",
#                     re.compile(r"several[ \-]<Q:F>([0-9]+)</Q:F>"),
#                     lambda m: f"<Q:F>{SEVERAL[0] * int(m.group(1))}</Q:F> to <Q:F>{SEVERAL[1] * int(m.group(1))}</Q:F>"
#                     )
# _FEW_TO_F = ("few-to-f",
#              re.compile(r"[Aa] few"),
#              lambda m: f"<Q:F>{FEW[0]}</Q:F> to <Q:F>{FEW[1]}</Q:F>"
#              )
_COUPLE_TO_F = ("couple-to-f",
                re.compile(r"[Aa] couple of"),
                lambda m: f"<Q:F>{COUPLE}</Q:F> of"
                )
# _SEVERAL_TO_F = ("several-to-f",
#                  re.compile(r"several(?: of)?"),
#                  lambda m: f"<Q:F>{SEVERAL[0]}</Q:F> to <Q:F>{SEVERAL[1]}</Q:F> of"
#                  )
_F_NEG = ("f-neg",
          re.compile("(?:negative|minus|neg) ?<Q:F>([0-9]+)</Q:F>"),
          r"<Q:F>-\1</Q:F>"
          )
_DECODE = ("decode",
           re.compile("<Q:F>([0-9\-]+)</Q:F>"),
           r"\1"
           )

_JOIN_PATTERNS = [
    _U_CONCAT_T,
    _T_CONCAT_T,
    _T_ADD_U,
    _U_MULT_S,
    _U_TO_R,
    _R_MULT_S,
    _R_ADD_R,
    _R_ADD_U,
    _S_ADD_R,
    _R_FINAL,
    _S_FINAL,
    _U_FINAL,
    _T_FINAL,
    _COUPLE_F,
    #_FEW_SPLIT_F,
    #_SEVERAL_SPLIT_F,
    _COUPLE_TO_F,
    #_FEW_TO_F,
    #_SEVERAL_TO_F,
    _F_NEG,
    _DECODE
]


def _encode(s, _debug=False):
    _s = s

    for lower, pattern, value in TENS:
        _s_pre = _s
        _s = re.sub(pattern, _enc_ten(value), _s)
        if _debug:
            if _s != _s_pre:
                print(_s)
    for lower, pattern, value in UNITS:
        _s_pre = _s
        _s = re.sub(pattern, _enc_unit(value), _s)
        if _debug:
            if _s != _s_pre:
                print(_s)
    for lower, pattern, value in SCALES:
        _s_pre = _s
        _s = re.sub(pattern, _enc_scale(value), _s)
        if _debug:
            if _s != _s_pre:
                print(_s)
    return _s


def _decode(s, _debug=False):
    _s = s
    for name, pattern, repl in _JOIN_PATTERNS:
        _s_pre = None
        while _s_pre != _s:
            _s_pre = _s
            _s = re.sub(pattern, repl, _s)
            if _debug:
                if _s_pre != _s:
                    print(name, _s)
    return _s


def quantify(s):
    return _decode(_encode(s))

words_to_numeric = Processor(
    id="regex-num-quantify",
    method=quantify
)