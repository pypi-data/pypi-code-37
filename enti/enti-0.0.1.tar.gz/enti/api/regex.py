import re
__all__ = [
    "_cx_",
    "_ca_",
    "_cc_",
    "_cw_",
    "_ch_",
    "_re_",
    "_sw_",
    "_sx_",
    "_ws_",
    "_wh_",
    "_jo_",
    "_jw_",
    "_opt_",
    "_sp_p_",
    "_rm_ws_",
    "_an_",
    "_flat_"
]

_cx_ = re_char_reserved = "\[\]()<>_"
_ca_ = re_char_alphanumeric = "a-zA-Z0-9"
_cc_ = re_func_concat = lambda x: "".join(x)
_cw_ = re_func_concat_ws = lambda x: _ws_("").join(x)
_ch_ = re_func_concat_hyphen = lambda x: _wh_("-").join(x)
_re_ = re_func_compile = lambda x: re.compile(x) if (isinstance(x, str)) else x
_sw_ = re_func_safe_wrap = lambda s: f"(?<!{_cx_}){s}(?!{_cx_})"
_sx_ = re_func_safe_wrap_strict = lambda s: f"(?<!{_cx_}{_ca_}){s}(?!{_cx_}{_ca_})"
_ws_ = re_func_opt_ws_repl = lambda s: re.sub(re.compile(f"{r'[ ]+'}"), r" ?", s)
_wh_ = re_func_opt_ws_hyphen_repl = lambda s: re.sub(re.compile(f"{r'[- ]+'}"), r" ?-? ?", s)
_jo_ = re_func_join_opts = lambda l: f"(?:{'|'.join(l)})"
_jw_ = re_func_join_opts_ws = lambda l: _jo_([_ws_(x) for x in l])
_opt_ = re_func_optional = lambda s: f"(?:{s})?"
_sp_p_ = re_func_suppress_paren = lambda s: re.sub(re.compile(r"\(.*\)"),"",s)
_rm_ws_ = re_func_strip_ws = lambda s: re.sub(r"\s", "", s)
_an_ = lambda x: re.sub(_re_(f"[^{_ca_}]"), "", x)
_flat_ = lambda l: [item for sublist in l for item in sublist]
