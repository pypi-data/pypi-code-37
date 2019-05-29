import kivy
#kivy.require('1.10.0') # replace with your current Kivy version

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.factory import Factory


class PlayPauseButton(ButtonBehavior, Image):

    def __init__(self, **kwargs):
        super(PlayPauseButton, self).__init__(**kwargs)
        self.playing = True
        self.set_button(False)

    def set_button(self, playing=True):
        if self.playing != playing:
            self.playing = playing
            self.source = 'atlas://data/icons/pause' if playing else 'atlas://data/icons/play'

    def on_press(self):
        self.set_button(not self.playing)



Factory.register("PlayPauseButton", cls=PlayPauseButton)
