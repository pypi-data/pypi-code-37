from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class CalendarDaily(VuetifyWidget):

    _model_name = Unicode('CalendarDailyModel').tag(sync=True)

    color = Unicode(None, allow_none=True).tag(sync=True)

    dark = Bool(None, allow_none=True).tag(sync=True)

    end = Unicode(None, allow_none=True).tag(sync=True)

    first_interval = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    hide_header = Bool(None, allow_none=True).tag(sync=True)

    interval_count = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    interval_height = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    interval_minutes = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    light = Bool(None, allow_none=True).tag(sync=True)

    locale = Unicode(None, allow_none=True).tag(sync=True)

    max_days = Float(None, allow_none=True).tag(sync=True)

    now = Unicode(None, allow_none=True).tag(sync=True)

    short_intervals = Bool(None, allow_none=True).tag(sync=True)

    short_weekdays = Bool(None, allow_none=True).tag(sync=True)

    start = Unicode(None, allow_none=True).tag(sync=True)

    weekdays = List(Any(), default_value=None, allow_none=True).tag(sync=True)





__all__ = ['CalendarDaily']
