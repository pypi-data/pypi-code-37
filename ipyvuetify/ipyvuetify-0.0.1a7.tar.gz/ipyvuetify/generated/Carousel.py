from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class Carousel(VuetifyWidget):

    _model_name = Unicode('CarouselModel').tag(sync=True)

    active_class = Unicode(None, allow_none=True).tag(sync=True)

    cycle = Bool(None, allow_none=True).tag(sync=True)

    dark = Bool(None, allow_none=True).tag(sync=True)

    delimiter_icon = Unicode(None, allow_none=True).tag(sync=True)

    height = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    hide_controls = Bool(None, allow_none=True).tag(sync=True)

    hide_delimiters = Bool(None, allow_none=True).tag(sync=True)

    interval = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    light = Bool(None, allow_none=True).tag(sync=True)

    mandatory = Bool(None, allow_none=True).tag(sync=True)

    max = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    multiple = Bool(None, allow_none=True).tag(sync=True)

    next_icon = Union([
        Bool(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    prev_icon = Union([
        Bool(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    reverse = Bool(None, allow_none=True).tag(sync=True)

    touch = Dict(default_value=None, allow_none=True).tag(sync=True)

    touchless = Bool(None, allow_none=True).tag(sync=True)

    value = Any(None, allow_none=True).tag(sync=True)

    vertical = Bool(None, allow_none=True).tag(sync=True)





__all__ = ['Carousel']
