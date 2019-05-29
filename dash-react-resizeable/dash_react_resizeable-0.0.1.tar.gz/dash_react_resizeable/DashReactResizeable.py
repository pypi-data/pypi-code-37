# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashReactResizeable(Component):
    """A DashReactResizeable component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- id (string; optional): The ID used to identify this component in Dash callbacks
- width (number; optional): The width of the resizable box
- height (number; optional): The height of the resizable box
- resizeHandles (list; optional): The array of resize handles that is activated
The full list is ['sw', 'se', 'nw', 'ne', 'w', 'e', 'n', 's']
- className (string; optional): The class of the input element"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, resizeHandles=Component.UNDEFINED, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'width', 'height', 'resizeHandles', 'className']
        self._type = 'DashReactResizeable'
        self._namespace = 'dash_react_resizeable'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'width', 'height', 'resizeHandles', 'className']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashReactResizeable, self).__init__(children=children, **args)
