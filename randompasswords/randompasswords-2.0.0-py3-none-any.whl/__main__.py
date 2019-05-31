#__main__.py for randompasswords

from randompasswords.InputFrame import *
import wx

def main():

    #fake = Faker()
    app = wx.App()
    frame = InputFrame()
    app.MainLoop()

if __name__ == "__main__":
    main()
