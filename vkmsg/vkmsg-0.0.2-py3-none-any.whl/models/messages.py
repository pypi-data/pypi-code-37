from .keyboards import Keyboard


class Message(object):
    def __init__(self, message: str, keyboard: Keyboard = None):
        if not isinstance(message, str):
            raise TypeError('message must be an instance of str')
        if keyboard is not None:
            if not isinstance(keyboard, Keyboard):
                raise TypeError('keyboard must be an instance of Keyboard')
        self.message = message
        self.keyboard = keyboard

    def to_dict(self):
        res = {
            'message': self.message,
        }
        if self.keyboard:
            res['keyboard'] = self.keyboard.to_dict()
        return res