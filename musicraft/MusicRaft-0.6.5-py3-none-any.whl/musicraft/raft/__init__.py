#!/usr/bin/python3
"""
Copyright 2016 Hippos Technical Systems BV.

@author: larry
"""
import sys
from .editbook import EditBook
from ..share import (Share, Signal, dbg_print, QtCore, QtWidgets, QtWidgets, QtSvg, WithMenu)
from .external import (StdOut, StdErr)
#import qdarkstyle

class StdBook(QtWidgets.QTabWidget):
    headerText = 'error/diagnostic output'
    whereDockable   = QtCore.Qt.AllDockWidgetAreas

    def __init__(self, dock=None):
        QtWidgets.QTabWidget.__init__(self)

class DisplayBook(QtWidgets.QTabWidget):
    pass  # for now
class Dock(QtWidgets.QDockWidget):
    def __init__(self, widgetClass, visible=True):
        QtWidgets.QDockWidget.__init__(self, widgetClass.headerText)
        self.setAllowedAreas(widgetClass.whereDockable)
        self.widget = widgetClass(dock=self)
        self.setWidget(self.widget)
        self.setVisible(visible)


class Raft(QtWidgets.QMainWindow, WithMenu):
    menuTag = '&File'

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Share.raft = self
        self.resize(1280, 1024)
        self.editBookDock = Dock(EditBook, True)
        self.editBookDock.setMinimumHeight(720)
        # self.raftEditor.setMinimumWidth(320)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.editBookDock)
        self.editBook = self.editBookDock.widget
        self.stdBook = Dock(StdBook,  True)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.stdBook)
        self.stdBook.setMinimumHeight(80)
        #sys.stdout = StdOut()
        #sys.stderr = StdErr()
        print ("testing stdout...", file=sys.stdout)
        print ("testing stderr...", file=sys.stderr)
        #sys.exit(0)
        self.createMenus()
        self.displayBook = DisplayBook()
        self.setCentralWidget(self.displayBook)
        #self.displayBook.setBaseSize(640, 480)
        #self.displayBook.addTab(QtWidgets.QGraphicsView(), "test widget")
        WithMenu.__init__(self)


    def start(self):
        self.show()
        self.editBook.openThemAll(sys.argv[1:])

    def about(self):
        QtWidgets.QMessageBox.about(self, "About 'Raft'",
                "<p>To be updated!.</p>"
                "<p></p>")

    def createMenus(self):
        self.helpMenu = QtWidgets.QMenu("&Help", self)
        self.aboutAct = self.myQAction("About &Raft", triggered=self.about)
        self.aboutQtAct = self.myQAction("About &Qt", triggered=QtWidgets.qApp.aboutQt)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)
        self.helpAction = self.menuBar().addMenu(self.helpMenu)

    def closeEvent(self, e):
        self.editBook.exit_etc()

    def menuItems(self):
        return [
                    ('&New',           'Ctrl+N', self.editBook.newFile,),
                    ('&Open',          'Ctrl+O', self.editBook.loadAnyFile,),
                    ('&Close',         'Ctrl+C', self.editBook.closeFile,),
                    #('Open in new &Instance', 'Ctrl+I', self.editor.cloneAnyFile,),
                    ('&Reload',        'Ctrl+R', self.editBook.reloadFile,),
                    ('R&estart',       'Ctrl+E', self.editBook.restart,),
                    ('&Save',          'Ctrl+S', self.editBook.saveFile,),
                    ('Save &As',       'Ctrl+A', self.editBook.saveFileAs,),
                    ('E&xit',          'Ctrl+Q', self.editBook.exit_etc),
                    ('&Transpose',     'Ctrl+T', self.editBook.transpose,),
#                    ('Set &Font', 'F', self.changeMyFont,),

        ]

def main(Plugins=()):
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    Raft()
    Share.plugins = []
    for Plugin in Plugins:
        try:
            Share.plugins.append(Plugin())
        except TypeError as exc:
            print(exc, file=sys.stderr)

    Share.raft.start()
    try:
        sys.exit(app.exec_())
    except:
        pass

if __name__ == '__main__':
    main()
