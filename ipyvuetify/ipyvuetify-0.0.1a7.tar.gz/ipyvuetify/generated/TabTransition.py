from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class TabTransition(VuetifyWidget):

    _model_name = Unicode('TabTransitionModel').tag(sync=True)

    group = Bool(None, allow_none=True).tag(sync=True)

    hide_on_leave = Bool(None, allow_none=True).tag(sync=True)

    leave_absolute = Bool(None, allow_none=True).tag(sync=True)

    mode = Unicode(None, allow_none=True).tag(sync=True)

    origin = Unicode(None, allow_none=True).tag(sync=True)





__all__ = ['TabTransition']
