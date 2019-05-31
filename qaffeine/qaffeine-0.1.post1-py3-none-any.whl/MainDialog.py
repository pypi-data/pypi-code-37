#
# qaffeine - prevent inactivity on your computer by simulating key events
#
# Clem Lorteau - 2019-05-26

import os
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, Qt, SIGNAL
from PySide2.QtWidgets import QDialog, QMessageBox
from PySide2.QtGui import QIcon
from src.KeyPressesSender import keys
from src.__init__ import __version__

path = os.path.dirname(os.path.realpath(__file__))

class MainDialog():

    ui = None
    
    @staticmethod
    def create():
        uifilename = path + '/res/maindialog.ui'
        uifile = QFile(os.path.join(path, uifilename))
        uifile.open(QFile.ReadOnly)
        loader = QUiLoader()
        MainDialog.ui = loader.load(uifile)
        uifile.close()

        MainDialog.ui.setWindowFlags(MainDialog.ui.windowFlags() & ~Qt.WindowContextHelpButtonHint \
                                           & ~Qt.WindowMaximizeButtonHint)
        MainDialog.ui.setWindowIcon(QIcon(path + '/' + 'res/icon_color.png'))
        MainDialog.ui.iconColorCombo.addItem(QIcon(path + '/' + 'res/icon_white_on.png'), 'white')
        MainDialog.ui.iconColorCombo.addItem(QIcon(path + '/' + 'res/icon_black_on.png'), 'black')
        MainDialog.ui.keysCombo.addItems(keys)
        MainDialog.ui.connect(MainDialog.ui.aboutButton, SIGNAL('clicked()'), MainDialog.showAbout)

        return MainDialog.ui
    
    @staticmethod
    def showAbout():
        if MainDialog.ui != None:
            text ='<b>qaffeine v' + __version__ + '</b><br/><br/>' + \
                  'Prevent inactivity by simulating key presses<br/><br/>' + \
                  '<i>Clem Lorteau 2019 - https://github.com/clorteau/qaffeine</i>'
            QMessageBox.about(MainDialog.ui, 'About qaffeine', text)

        
