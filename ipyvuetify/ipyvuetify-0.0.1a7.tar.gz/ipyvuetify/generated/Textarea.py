from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class Textarea(VuetifyWidget):

    _model_name = Unicode('TextareaModel').tag(sync=True)

    append_icon = Unicode(None, allow_none=True).tag(sync=True)

    append_outer_icon = Unicode(None, allow_none=True).tag(sync=True)

    auto_grow = Bool(None, allow_none=True).tag(sync=True)

    autofocus = Bool(None, allow_none=True).tag(sync=True)

    background_color = Unicode(None, allow_none=True).tag(sync=True)

    box = Bool(None, allow_none=True).tag(sync=True)

    browser_autocomplete = Unicode(None, allow_none=True).tag(sync=True)

    clear_icon = Unicode(None, allow_none=True).tag(sync=True)

    clearable = Bool(None, allow_none=True).tag(sync=True)

    color = Unicode(None, allow_none=True).tag(sync=True)

    counter = Union([
        Bool(),
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    dark = Bool(None, allow_none=True).tag(sync=True)

    disabled = Bool(None, allow_none=True).tag(sync=True)

    dont_fill_mask_blanks = Bool(None, allow_none=True).tag(sync=True)

    error = Bool(None, allow_none=True).tag(sync=True)

    error_count = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    error_messages = Union([
        Unicode(),
        List(Any())
    ], default_value=None, allow_none=True).tag(sync=True)

    flat = Bool(None, allow_none=True).tag(sync=True)

    full_width = Bool(None, allow_none=True).tag(sync=True)

    height = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    hide_details = Bool(None, allow_none=True).tag(sync=True)

    hint = Unicode(None, allow_none=True).tag(sync=True)

    label = Unicode(None, allow_none=True).tag(sync=True)

    light = Bool(None, allow_none=True).tag(sync=True)

    loading = Union([
        Bool(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    mask = Union([
        Dict(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    messages = Union([
        Unicode(),
        List(Any())
    ], default_value=None, allow_none=True).tag(sync=True)

    no_resize = Bool(None, allow_none=True).tag(sync=True)

    outline = Bool(None, allow_none=True).tag(sync=True)

    persistent_hint = Bool(None, allow_none=True).tag(sync=True)

    placeholder = Unicode(None, allow_none=True).tag(sync=True)

    prefix = Unicode(None, allow_none=True).tag(sync=True)

    prepend_icon = Unicode(None, allow_none=True).tag(sync=True)

    prepend_inner_icon = Unicode(None, allow_none=True).tag(sync=True)

    readonly = Bool(None, allow_none=True).tag(sync=True)

    return_masked_value = Bool(None, allow_none=True).tag(sync=True)

    reverse = Bool(None, allow_none=True).tag(sync=True)

    row_height = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    rows = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    rules = List(Any(), default_value=None, allow_none=True).tag(sync=True)

    single_line = Bool(None, allow_none=True).tag(sync=True)

    solo = Bool(None, allow_none=True).tag(sync=True)

    solo_inverted = Bool(None, allow_none=True).tag(sync=True)

    success = Bool(None, allow_none=True).tag(sync=True)

    success_messages = Union([
        Unicode(),
        List(Any())
    ], default_value=None, allow_none=True).tag(sync=True)

    suffix = Unicode(None, allow_none=True).tag(sync=True)

    type = Unicode(None, allow_none=True).tag(sync=True)

    validate_on_blur = Bool(None, allow_none=True).tag(sync=True)

    value = Any(None, allow_none=True).tag(sync=True)





__all__ = ['Textarea']
