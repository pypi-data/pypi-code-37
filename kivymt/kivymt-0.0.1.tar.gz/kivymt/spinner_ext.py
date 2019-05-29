'''
SpinnerExt
==========

.. versionadded:: 1.10.0

SpinnerExt is a widget that provides a quick way to select one value from a set,
and additionally an option to insert a new value. SpinnerExt is a variant of the
kivy.uix.Spinner class.
In the default state, a spinner shows its currently selected value.
Touching the spinner displays a dropdown menu with all the other available
values from which the user can select a new one. After the last option, there is
one extra option to insert a new value.

Example::

    from kivy.base import runTouchApp
    from kivymt.spinner_ext import SpinnerExt

    spinner = SpinnerExt(
        # default value shown
        text='Home',
        # available values
        values=('Home', 'Work', 'Other', 'Custom'),
        # just for positioning in our example
        size_hint=(None, None),
        size=(100, 44),
        pos_hint={'center_x': .5, 'center_y': .5})

    def show_selected_value(spinner, text):
        print('The spinner', spinner, 'have text', text)

    spinner.bind(text=show_selected_value)

    runTouchApp(spinner)

'''

__all__ = ('SpinnerExt', 'SpinnerOption')

from kivy.compat import string_types
from kivy.factory import Factory
from kivy.properties import ListProperty, ObjectProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import SpinnerOption


class SpinnerExt(Button):
    '''SpinnerExt class, see module documentation for more information.
    '''

    values = ListProperty()
    '''Values that can be selected by the user. It must be a list of strings.

    :attr:`values` is a :class:`~kivy.properties.ListProperty` and defaults to
    [].
    '''

    option_cls = ObjectProperty(SpinnerOption)
    '''Class used to display the options within the dropdown list displayed
    under the SpinnerExt. The `text` property of the class will be used to
    represent the value.

    The option class requires:

    - a `text` property, used to display the value.
    - an `on_release` event, used to trigger the option when pressed/touched.
    - a :attr:`~kivy.uix.widget.Widget.size_hint_y` of None.
    - the :attr:`~kivy.uix.widget.Widget.height` to be set.

    :attr:`option_cls` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to :class:`SpinnerOption`.

    .. versionchanged:: 1.8.0
        If you set a string, the :class:`~kivy.factory.Factory` will be used to
        resolve the class.

    '''

    dropdown_cls = ObjectProperty(DropDown)
    '''Class used to display the dropdown list when the SpinnerExt is pressed.

    :attr:`dropdown_cls` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to :class:`~kivy.uix.dropdown.DropDown`.

    .. versionchanged:: 1.8.0
        If set to a string, the :class:`~kivy.factory.Factory` will be used to
        resolve the class name.

    '''

    is_open = BooleanProperty(False)
    '''By default, the spinner is not open. Set to True to open it.

    :attr:`is_open` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to False.

    .. versionadded:: 1.4.0
    '''

    sync_height = BooleanProperty(False)
    '''Each element in a dropdown list uses a default/user-supplied height.
    Set to True to propagate the SpinnerExt's height value to each dropdown
    list element.

    .. versionadded:: 1.10.0

    :attr:`sync_height` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to False.
    '''

    def __init__(self, **kwargs):
        self._dropdown = None
        super(SpinnerExt, self).__init__(**kwargs)
        fbind = self.fbind
        build_dropdown = self._build_dropdown
        fbind('on_release', self._toggle_dropdown)
        fbind('dropdown_cls', build_dropdown)
        fbind('option_cls', build_dropdown)
        fbind('values', self._update_dropdown)
        fbind('size', self._update_dropdown_size)
        build_dropdown()

    def _build_dropdown(self, *largs):
        if self._dropdown:
            self._dropdown.unbind(on_select=self._on_dropdown_select)
            self._dropdown.unbind(on_dismiss=self._close_dropdown)
            self._dropdown.dismiss()
            self._dropdown = None
        cls = self.dropdown_cls
        if isinstance(cls, string_types):
            cls = Factory.get(cls)
        self._dropdown = cls()
        self._dropdown.bind(on_select=self._on_dropdown_select)
        self._dropdown.bind(on_dismiss=self._close_dropdown)
        self._update_dropdown()

    def _update_dropdown_size(self, *largs):
        if not self.sync_height:
            return
        dp = self._dropdown
        if not dp:
            return

        container = dp.container
        if not container:
            return
        h = self.height
        for item in container.children[:]:
            item.height = h

    def _update_dropdown(self, *largs):
        dp = self._dropdown
        cls = self.option_cls
        values = self.values
        if isinstance(cls, string_types):
            cls = Factory.get(cls)
        dp.clear_widgets()

        # static values
        min_item_height = None
        for value in values:
            item = cls(text=value)
            item.height = self.height if self.sync_height else item.height
            if min_item_height is None or min_item_height > item.height:
                min_item_height = item.height
            item.bind(on_release=lambda option: dp.select(option.text))
            dp.add_widget(item)
        if min_item_height is None:
            min_item_height = 100

        # editable item
        item = TextInput(text='', multiline=False, size_hint_y=None)
        item.height = self.height if self.sync_height else min_item_height
        item.bind(on_text_validate=lambda option: dp.select(option.text))
        dp.add_widget(item)

    def _toggle_dropdown(self, *largs):
        if self.values:
            self.is_open = not self.is_open

    def _close_dropdown(self, *largs):
        self.is_open = False

    def _on_dropdown_select(self, instance, data, *largs):
        self.text = data
        self.is_open = False

    def on_is_open(self, instance, value):
        if value:
            self._dropdown.open(self)
        else:
            if self._dropdown.attach_to:
                self._dropdown.dismiss()



Factory.register("SpinnerExt", cls=SpinnerExt)
