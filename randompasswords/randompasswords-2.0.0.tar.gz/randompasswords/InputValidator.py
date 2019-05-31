import wx


class StringValidator(wx.Validator):
    def __init__(self):
        super().__init__()

    def Clone(self):
        return StringValidator()

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if all(c.isalnum() or c.isspace() for c in text):
            return True
        else:
            wx.MessageBox("Only alphanumeric characters separated by [SPACE] allowed!",
                          "Invalid Input", wx.OK | wx.ICON_ERROR)
            return False


class NumberValidator(wx.Validator):
    def __init__(self):
        super().__init__()

    def Clone(self):
        return NumberValidator()

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return False

    def Validate(self, win):
        textCtrl = win.GetWindow()
        text = win.GetValues()


        if all(n.isdigit() for n in text):
            return True
        else:
            wx.MessageBox("Only numbers allowed!", "Invalid Input",
                          wx.OK | wx.ICON_ERROR)
            return False
