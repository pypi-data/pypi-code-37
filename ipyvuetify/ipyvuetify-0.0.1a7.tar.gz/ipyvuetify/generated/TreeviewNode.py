from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class TreeviewNode(VuetifyWidget):

    _model_name = Unicode('TreeviewNodeModel').tag(sync=True)

    activatable = Bool(None, allow_none=True).tag(sync=True)

    active_class = Unicode(None, allow_none=True).tag(sync=True)

    expand_icon = Unicode(None, allow_none=True).tag(sync=True)

    indeterminate_icon = Unicode(None, allow_none=True).tag(sync=True)

    item = Dict(default_value=None, allow_none=True).tag(sync=True)

    item_children = Unicode(None, allow_none=True).tag(sync=True)

    item_key = Unicode(None, allow_none=True).tag(sync=True)

    item_text = Unicode(None, allow_none=True).tag(sync=True)

    loading_icon = Unicode(None, allow_none=True).tag(sync=True)

    off_icon = Unicode(None, allow_none=True).tag(sync=True)

    on_icon = Unicode(None, allow_none=True).tag(sync=True)

    open_on_click = Bool(None, allow_none=True).tag(sync=True)

    selectable = Bool(None, allow_none=True).tag(sync=True)

    selected_color = Unicode(None, allow_none=True).tag(sync=True)

    transition = Bool(None, allow_none=True).tag(sync=True)





__all__ = ['TreeviewNode']
