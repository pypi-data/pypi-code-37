#
# qaffeine - prevent inactivity on your computer by simulating key events
#
# Clem Lorteau - 2019-05-26

import sys
import os
from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QMessageBox, QMenu, QAction, QToolTip
from PySide2.QtGui import QIcon, QCursor
from PySide2.QtCore import SIGNAL, Qt, QSettings
from src.MainDialog import MainDialog
from threading import Event
from src.KeyPressesSender import KeyPressesSender

path = os.path.dirname(os.path.realpath(__file__))

class UI():
    
    def __init__(self):

        # Application object
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # settings dialog
        self.mainDialog = MainDialog.create()
        self.mainDialog.connect(self.mainDialog.closeButton, SIGNAL('clicked()'), self.doCloseDialog)
        self.mainDialog.connect(self.mainDialog.saveButton, SIGNAL('clicked()'), self.doSave)
        
        self.settings = QSettings('qaffeine', 'config')

        if (self.settings.value('delay')):
            self.delay = self.settings.value('delay')
        else:
            self.delay = '5'
        self.mainDialog.delaySpinBox.setValue(int(self.delay))

        if (self.settings.value('key')):
            self.key = self.settings.value('key')
        else:
            self.key = 'altright'
        self.mainDialog.keysCombo.setCurrentText(self.key)

        if (self.settings.value('iconTheme')):
            self.iconTheme = self.settings.value('iconTheme')
        else:
            self.iconTheme = 'white'
        self.mainDialog.iconColorCombo.setCurrentText(self.iconTheme)

        # inactivity blocker thread
        self.stopFlag = Event()
        self.stopFlag.set()
        self.thread = KeyPressesSender(self.stopFlag, self.key, self.delay)

        # system tray
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(None, 'Error', 'No notification area found; this application can\'t run without one', )
        else:
            self.systray = QSystemTrayIcon(parent=self.mainDialog)
            self.menu = QMenu()

            self.activateAction = QAction('&Activate', self.systray)
            self.systray.connect(self.activateAction, SIGNAL('triggered()'), self.doActivateAction)
            self.menu.addAction(self.activateAction)

            self.menu.addSeparator()

            settingsAction = QAction('&Settings', self.systray)
            self.systray.connect(settingsAction, SIGNAL('triggered()'), self.doSettingsAction)
            self.menu.addAction(settingsAction)

            self.menu.addSeparator()

            quitAction = QAction('&Quit', self.systray)
            self.systray.connect(quitAction, SIGNAL('triggered()'), self.doQuitAction)
            self.menu.addAction(quitAction)

            self.systray.setContextMenu(self.menu)
            self.systray.setIcon(QIcon(path + '/' + 'res/icon_' + self.iconTheme + '_off.png'))
            self.systray.activated.connect(self.doSystrayActivated)
            self.systray.setVisible(True)

    def doCloseDialog(self):
        self.key = self.mainDialog.keysCombo.currentText()
        self.delay = self.mainDialog.delaySpinBox.value()
        self.iconTheme = self.mainDialog.iconColorCombo.currentText()
        self.mainDialog.setVisible(False)

    def doSave(self):
        self.settings.setValue('key', self.mainDialog.keysCombo.currentText())
        self.settings.setValue('delay', self.mainDialog.delaySpinBox.value())
        self.settings.setValue('iconTheme', self.mainDialog.iconColorCombo.currentText())
        toolTip = QToolTip()
        toolTip.showText(QCursor.pos(), 'Saved')

    def doSystrayActivated(self):
        # Open menu on any click, not just right click
        self.menu.exec_(QCursor.pos())

    def doQuitAction(self):
        self.stopFlag.set()
        sys.exit(0)

    def doSettingsAction(self):
        self.mainDialog.show()

    def doActivateAction(self):
        if self.stopFlag.is_set():
            print('Starting inactivity prevention')
            self.systray.setIcon(QIcon(path + '/' + 'res/icon_' + self.iconTheme + '_on.png'))
            self.stopFlag.clear()
            self.thread.key = self.key
            self.thread.delay = int(self.delay)
            self.thread.start()
            self.activateAction.setText('St&op')
        else: 
            self.systray.setIcon(QIcon(path + '/' + 'res/icon_' + self.iconTheme + '_off.png'))
            print('Stopping inactivity prevention')
            self.stopFlag.set()
            self.activateAction.setText('&Activate')
    
    def start(self):
        self.systray.show()
        sys.exit(self.app.exec_())

