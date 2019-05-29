'''
DatetimeEditor
==============

.. versionadded:: 1.10.0

DatetimeEditor is a widget that provides a quick way to edit both
date and time. It is essentially a text input but when focused, will
open a popup where you can pick date and time interactively. At the
bottom of the popup, there is a real text input where you can manually
enter date and time in the standard format. The datetime is precised
up to second level and is represented by Python's `datetime` class.

Example::

    from kivy.base import runTouchApp
    from kivymt.datetime_editor import DatetimeEditor
    from datetime import datetime

    dt_editor = DatetimeEditor(
        dt=datetime.now(), # input/output datetime
        pHint=(0.8,0.4) # popup size hint
        # just for positioning in our example
        size_hint=(None, None),
        size=(100, 44),
        pos_hint={'center_x': .5, 'center_y': .5})

    def show_selected_value(dt_editor, dt):
        print('The dt_editor', spinner, 'has datetime', dt)

    dt_editor.bind(dt=show_selected_value)

    runTouchApp(dt_editor)

'''

__all__ = ('DatetimeEditor',)

from datetime import datetime

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ListProperty, ReferenceListProperty, ObjectProperty, BooleanProperty, StringProperty, NumericProperty, AliasProperty
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivymt.image_btn import ImageButton
from kivymt.calendar import CalendarWidget
from kivymt.circulardatetimepicker import CircularTimeWidget


# ---------- DatetimeEditorPopup ----------


Builder.load_string("""
#:import CalendarWidget      kivymt.calendar.CalendarWidget
#:import CircularTimeWidget  kivymt.circulardatetimepicker.CircularTimeWidget

<DatetimeEditorPopup>:
    title: "Date and time"

    BoxLayout:
        orientation: "vertical"

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 1

            Button:
                id: wdg_set_date_today
                text: "Set date today"
                size_hint_x: 1
                on_release: root.on_set_date_today()

            Button:
                id: wdg_set_time_now
                text: "Set time now"
                size_hint_x: 1
                on_release: root.on_set_time_now()

            Button:
                id: wdg_reset-time
                text: "Reset time"
                size_hint_x: 1
                on_release: root.on_reset_time()

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 6

            CalendarWidget:
                id: wdg_date
                size_hint_x: 1

            CircularTimeWidget:
                id: wdg_time
                size_hint_x: 1

        TextInput:
            id: wdg_text
            size_hint_y: 1
            multiline: False
            on_text_validate: root.on_text_validate()

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 1

            Button:
                id: wdg_ok
                text: "OK"
                size_hint_x: 1
                on_release: root.on_ok()

            Button:
                id: wdg_cancel
                text: "Cancel"
                size_hint_x: 1
                on_release: root.on_cancel()
""")


class DatetimeEditorPopup(Popup):

    _dt = datetime.now()
    def _get_dt(self):
        return self._dt
    def _set_dt(self, dt):
        if not isinstance(dt, datetime):
            raise ValueError("Unable to set a non-datetime value to a datetime property.")
        self._dt = dt
        if len(self.ids) > 0:
            if self.ids.wdg_date.active_date != [dt.day, dt.month, dt.year]:
                self.ids.wdg_date.active_date = [dt.day, dt.month, dt.year]
            if self.ids.wdg_time.time != dt.time():
                self.ids.wdg_time.time = dt.time()
            text = dt.strftime(self.format)
            if self.ids.wdg_text.text != text:
                self.ids.wdg_text.text = text
    dt = AliasProperty(_get_dt, _set_dt)
    """The current datetime record.

    :attr:`dt` is a :class:`~kivy.properties.AliasProperty` and
    defaults to datetime.now().
    """

    format = StringProperty("%Y-%m-%d %H:%M:%S")

    def __init__(self, dt=None, *args, **kwargs):
        super(DatetimeEditorPopup, self).__init__(*args, **kwargs)

        self.ids.wdg_date.bind(active_date=self.on_update_text_date)
        self.ids.wdg_time.bind(time=self.on_update_text_time)

        self.dt = dt
        self.old_dt = dt

        if not self.dt:
            self.dt = datetime.now()

    def on_text_validate(self):
        '''Handles the case when the new text needs validation.'''
        try:
            self.dt = datetime.strptime(self.ids.wdg_text.text, self.format)
        except:
            return

    def on_update_text_date(self, instance, value):
        '''Handles the case when the date widget has a new date.'''
        self.dt = datetime(value[2], value[1], value[0], self.dt.hour, self.dt.minute, self.dt.second)

    def on_update_text_time(self, instance, value):
        '''Handles the case when the time widget has a new time.'''
        self.dt = datetime(self.dt.year, self.dt.month, self.dt.day, value.hour, value.minute, value.second)

    def on_ok(self):
        '''Handles the case when the user clicks OK.'''
        self.on_text_validate()
        self.dismiss()

    def on_cancel(self):
        '''Handles the case when the user clicks Cancel.'''
        self.dt = self.old_dt
        self.dismiss()

    def on_set_date_today(self):
        '''Handles the case when the user wants today as the date.'''
        today = datetime.today()
        self.dt = datetime(today.year, today.month, today.day, self.dt.hour, self.dt.minute, self.dt.second)

    def on_set_time_now(self):
        '''Handles the case when the user wants now as the time.'''
        now = datetime.now()
        self.dt = datetime(self.dt.year, self.dt.month, self.dt.day, now.hour, now.minute, now.second)

    def on_reset_time(self):
        '''handles the case when the user wants reset the time but keep the date.'''
        self.dt = datetime(self.dt.year, self.dt.month, self.dt.day, 0, 0, 0)


# ---------- DatetimeEditor ----------


class DatetimeEditor(TextInput):
    """A TextInput but when focused, shows the DatetimeEditorPopup. You can
    define the popup dimensions using  pHint_x, pHint_y, and the pHint lists. 
    The `format` property formats the date and time to string using strftime() 
    and strptime(). The `dt` property can be used to initialise date and time.
    It is an ObjectProperty holding a Python datetime object.

    For example in kv:
    DatetimeEditor:
        dt: datetime(2017, 3, 2, 11, 22, 33)
        pHint: 0.7,0.4
        format: "%H:%M:%S"
    would result in a size_hint of 0.7,0.4 being used to create the popup
    """

    # ----- properties -----

    dt = ObjectProperty(None, allownone=True)
    '''Datetime that can be edited by the user. Must be None or of class datetime.

    :attr:`dt` is a :class:`~kivy.properties.ObjectProperty` and defaults to None.
    '''

    pHint_x = NumericProperty(0.8)
    pHint_y = NumericProperty(0.6)
    pHint = ReferenceListProperty(pHint_x ,pHint_y)
    '''Popup size hint that can be edited by the user.

    :attr:`pHint` is a :class:`~kivy.properties.ObjectProperty` and defaults to (0.8, 0.6).
    '''


    format = StringProperty("%Y-%m-%d %H:%M:%S")
    '''Datetime format to be used by strftime() and strptime().

    :attr:`format` is a :class:`~kivy.properties.StringPoperty` and defaults to "%Y-%m-%d %H:%M:%S".
    '''

    # ----- initialisation -----

    def __init__(self, *args, **kwargs):
        super(DatetimeEditor, self).__init__(*args, **kwargs)

        self.bind(focus=self.show_popup, dt=self.on_dt_changed)

        if not self.dt:
            self.dt = datetime.now()

        # Popup
        self.popup = DatetimeEditorPopup(on_dismiss=self.update_value, dt=self.dt)
        self.popup.format = self.format

    def on_dt_changed(self, inst, val):
        '''Handles the case where the dt has been changed.'''
        text = val.strftime(self.format)
        if text != self.text:
            self.text = text
        if hasattr(self, 'popup') and self.dt != self.popup.dt:
            self.popup.dt = self.dt

    def show_popup(self, isnt, val):
        """
        Open popup if textinput focused,
        and regardless update the popup size_hint
        """
        self.popup.size_hint=self.pHint
        if val:
            # Automatically dismiss the keyboard
            # that results from the textInput
            Window.release_all_keyboards()
            if self.dt != self.popup.dt:
                self.popup.dt = self.dt
            self.popup.open()

    def update_value(self, inst):
        """ Update textinput value on popup close """

        self.dt = self.popup.dt
        self.focus = False


Factory.register("DatetimeEditor", cls=DatetimeEditor)

