from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QIntValidator

from orangewidget.widget import OWBaseWidget as Widget, Output, Input
from orangewidget.settings import Setting
from orangewidget import gui


class IntNumber(Widget):
    # Widget's name as displayed in the canvas
    name = "Integer Number"
    # Short widget description
    description = "Lets the user input a number"

    # An icon resource file path for this widget
    # (a path relative to the module where this widget is defined)
    icon = "icons/number.svg"

    # Widget's outputs; here, a single output named "Number", of type int
    class Outputs:
        number = Output("Number", int)

    # Basic (convenience) GUI definition:
    #   a simple 'single column' GUI layout
    want_main_area = False
    #   with a fixed non resizable geometry.
    resizing_enabled = False

    number = Setting(42)

    def __init__(self):
        super().__init__()

        gui.lineEdit(self.controlArea, self, "number", "Enter a number",
                     box="Number",
                     callback=self.number_changed,
                     valueType=int, validator=QIntValidator())
        self.number_changed()

    def number_changed(self):
        # Send the entered number on "Number" output
        self.Outputs.number.send(self.number)


class Adder(Widget):
    name = "Add two integers"
    description = "Add two numbers"
    icon = "icons/add.svg"

    class Inputs:
        a = Input("A", int)
        b = Input("B", int)

    class Outputs:
        sum = Output("A + B", int)

    want_main_area = False

    def __init__(self):
        super().__init__()
        self.a = None
        self.b = None

    @Inputs.a
    def set_A(self, a):
        """Set input 'A'."""
        self.a = a

    @Inputs.b
    def set_B(self, b):
        """Set input 'B'."""
        self.b = b

    def handleNewSignals(self):
        """Reimplemeted from OWBaseWidget."""
        if self.a is not None and self.b is not None:
            self.Outputs.sum.send(self.a + self.b)
        else:
            # Clear the channel by sending `None`
            self.Outputs.sum.send(None)
