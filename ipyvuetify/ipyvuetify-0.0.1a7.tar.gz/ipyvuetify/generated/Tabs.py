from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class Tabs(VuetifyWidget):

    _model_name = Unicode('TabsModel').tag(sync=True)

    active_class = Unicode(None, allow_none=True).tag(sync=True)

    align_with_title = Bool(None, allow_none=True).tag(sync=True)

    centered = Bool(None, allow_none=True).tag(sync=True)

    color = Unicode(None, allow_none=True).tag(sync=True)

    dark = Bool(None, allow_none=True).tag(sync=True)

    fixed_tabs = Bool(None, allow_none=True).tag(sync=True)

    grow = Bool(None, allow_none=True).tag(sync=True)

    height = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    hide_slider = Bool(None, allow_none=True).tag(sync=True)

    icons_and_text = Bool(None, allow_none=True).tag(sync=True)

    light = Bool(None, allow_none=True).tag(sync=True)

    mandatory = Bool(None, allow_none=True).tag(sync=True)

    max = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    mobile_break_point = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    multiple = Bool(None, allow_none=True).tag(sync=True)

    next_icon = Unicode(None, allow_none=True).tag(sync=True)

    prev_icon = Unicode(None, allow_none=True).tag(sync=True)

    right = Bool(None, allow_none=True).tag(sync=True)

    show_arrows = Bool(None, allow_none=True).tag(sync=True)

    slider_color = Unicode(None, allow_none=True).tag(sync=True)

    value = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)





__all__ = ['Tabs']
