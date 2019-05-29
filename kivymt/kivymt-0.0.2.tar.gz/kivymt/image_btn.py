import kivy
#kivy.require('1.10.0') # replace with your current Kivy version

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.factory import Factory


class ImageButton(ButtonBehavior, Image):
    pass


Factory.register("ImageButton", cls=ImageButton)
