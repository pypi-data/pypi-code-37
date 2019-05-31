from randompasswords import InputValidator
from randompasswords.passwordgenerator import *
import wx

class InputFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Password Generator')

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.keywords_ctrl = wx.TextCtrl(panel, validator=InputValidator.StringValidator(),
                                         name='keyword_input',)
        self.keywords_ctrl.SetLabelText("Enter keywords separated by [SPACE]")
        self.min_ctrl = wx.TextCtrl(panel, validator=InputValidator.NumberValidator(),
                                    name='min_input',)
        self.min_ctrl.SetLabelText("Enter minimum length (default is 6)")
        self.max_ctrl = wx.TextCtrl(panel, validator=InputValidator.NumberValidator(),
                                    name='max_input',)
        self.max_ctrl.SetLabelText("Enter maximum length (default is 10)")
        self.special_ctrl = wx.TextCtrl(panel, name='special_input',)
        self.special_ctrl.SetLabelText("Enter special characters separated by [SPACE]")

        enter_button = wx.Button(panel, label='Generate Passwords')
        enter_button.Bind(wx.EVT_BUTTON, self.on_enter)

        sizer.Add(self.keywords_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.min_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.max_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.special_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(enter_button, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(sizer)

        self.Show()

    def on_enter(self, event):
        keywordslist = self.keywords_ctrl.GetValue()
        min = self.min_ctrl.GetValue()
        max = self.max_ctrl.GetValue()
        speciallist = self.special_ctrl.GetValue()

        if(min == ""):
            min = "6"
        if(max == ""):
            max = "10"
        # check input
        if(not min.isdigit() or not max.isdigit()):
            wx.MessageBox("Min and Max must be numbers!", "Invalid input", wx.OK | wx.ICON_ERROR)
            return False

        if(int(min) > int(max)):
            wx.MessageBox("Min must be less than max!", "Invalid input", wx.OK | wx.ICON_ERROR)
            return False

        if(speciallist.isalnum()):
            wx.MessageBox("Special characters can't contain alphanumeric characters!", "Invalid input",
                          wx.OK | wx.ICON_ERROR)
            return False

        if(keywordslist.endswith(" ")):
            keywordslist = keywordslist[:-1]

        keywords = keywordslist.replace(" ", "")
        special = speciallist.replace(" ", "")

        #wx.MessageBox(keywords + '\n' + str(min) + '\n' + str(max) + '\n' + special)

        passwords = generatePasswords(keywords, min, max, special)
        storePasswords(passwords)
        displayFrame = OutputFrame(passwords)
        displayFrame.Show()

#displays passwords in a list
class OutputFrame(wx.Frame):
    def __init__(self, passwordlist):
        super().__init__(parent=None, title='Random Passwords')
        panel = wx.Panel(self)
        self.list_ctrl = wx.ListCtrl(panel, -1, style=wx.LC_REPORT)

        self.list_ctrl.InsertColumn(0, '#')
        self.list_ctrl.InsertColumn(1, 'Passwords')
        self.list_ctrl.SetColumnWidth(1, 200)

        for index, pwlist in enumerate(passwordlist):
            pw = ''.join(pwlist)
            self.list_ctrl.InsertItem(index, str(index + 1))
            self.list_ctrl.SetItem(float(index), 1, pw, imageId=-1)









