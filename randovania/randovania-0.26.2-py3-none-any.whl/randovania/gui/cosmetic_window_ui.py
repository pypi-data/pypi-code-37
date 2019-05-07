# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/travis/build/randovania/randovania/randovania/gui/cosmetic_window.ui',
# licensing of '/home/travis/build/randovania/randovania/randovania/gui/cosmetic_window.ui' applies.
#
# Created: Tue May  7 20:31:40 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CosmeticWindow(object):
    def setupUi(self, CosmeticWindow):
        CosmeticWindow.setObjectName("CosmeticWindow")
        CosmeticWindow.resize(392, 405)
        self.centralWidget = QtWidgets.QWidget(CosmeticWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.seed_settings_warning_label = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.seed_settings_warning_label.sizePolicy().hasHeightForWidth())
        self.seed_settings_warning_label.setSizePolicy(sizePolicy)
        self.seed_settings_warning_label.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.seed_settings_warning_label.setFont(font)
        self.seed_settings_warning_label.setWordWrap(True)
        self.seed_settings_warning_label.setObjectName("seed_settings_warning_label")
        self.verticalLayout.addWidget(self.seed_settings_warning_label)
        self.faster_credits_check = QtWidgets.QCheckBox(self.centralWidget)
        self.faster_credits_check.setObjectName("faster_credits_check")
        self.verticalLayout.addWidget(self.faster_credits_check)
        self.faster_credits_label = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.faster_credits_label.sizePolicy().hasHeightForWidth())
        self.faster_credits_label.setSizePolicy(sizePolicy)
        self.faster_credits_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.faster_credits_label.setWordWrap(True)
        self.faster_credits_label.setObjectName("faster_credits_label")
        self.verticalLayout.addWidget(self.faster_credits_label)
        self.remove_hud_popup_check = QtWidgets.QCheckBox(self.centralWidget)
        self.remove_hud_popup_check.setObjectName("remove_hud_popup_check")
        self.verticalLayout.addWidget(self.remove_hud_popup_check)
        self.remove_hud_popup_label = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove_hud_popup_label.sizePolicy().hasHeightForWidth())
        self.remove_hud_popup_label.setSizePolicy(sizePolicy)
        self.remove_hud_popup_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.remove_hud_popup_label.setWordWrap(True)
        self.remove_hud_popup_label.setObjectName("remove_hud_popup_label")
        self.verticalLayout.addWidget(self.remove_hud_popup_label)
        self.open_map_check = QtWidgets.QCheckBox(self.centralWidget)
        self.open_map_check.setObjectName("open_map_check")
        self.verticalLayout.addWidget(self.open_map_check)
        self.open_map_label = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_map_label.sizePolicy().hasHeightForWidth())
        self.open_map_label.setSizePolicy(sizePolicy)
        self.open_map_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.open_map_label.setWordWrap(True)
        self.open_map_label.setObjectName("open_map_label")
        self.verticalLayout.addWidget(self.open_map_label)
        self.pickup_markers_check = QtWidgets.QCheckBox(self.centralWidget)
        self.pickup_markers_check.setObjectName("pickup_markers_check")
        self.verticalLayout.addWidget(self.pickup_markers_check)
        self.pickup_markers_label = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pickup_markers_label.sizePolicy().hasHeightForWidth())
        self.pickup_markers_label.setSizePolicy(sizePolicy)
        self.pickup_markers_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.pickup_markers_label.setWordWrap(True)
        self.pickup_markers_label.setObjectName("pickup_markers_label")
        self.verticalLayout.addWidget(self.pickup_markers_label)
        CosmeticWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(CosmeticWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 392, 21))
        self.menuBar.setObjectName("menuBar")
        CosmeticWindow.setMenuBar(self.menuBar)

        self.retranslateUi(CosmeticWindow)
        QtCore.QMetaObject.connectSlotsByName(CosmeticWindow)

    def retranslateUi(self, CosmeticWindow):
        CosmeticWindow.setWindowTitle(QtWidgets.QApplication.translate("CosmeticWindow", "Hello, world!", None, -1))
        self.seed_settings_warning_label.setText(QtWidgets.QApplication.translate("CosmeticWindow", "<html><head/><body><p><span style=\" color:#00aa00;\">All options in this tab can be freely changed without affecting the seed.</span></p></body></html>", None, -1))
        self.faster_credits_check.setText(QtWidgets.QApplication.translate("CosmeticWindow", "Faster Credits", None, -1))
        self.faster_credits_label.setText(QtWidgets.QApplication.translate("CosmeticWindow", "Speeds up the credits to be 60 seconds long (over 4x faster).", None, -1))
        self.remove_hud_popup_check.setText(QtWidgets.QApplication.translate("CosmeticWindow", "Skip Item Acquisition Popups", None, -1))
        self.remove_hud_popup_label.setText(QtWidgets.QApplication.translate("CosmeticWindow", "<html><head/><body><p>Replaces the &quot;Item Acquired&quot; popup after collecting an item with an alert.</p></body></html>", None, -1))
        self.open_map_check.setText(QtWidgets.QApplication.translate("CosmeticWindow", "Open map from start", None, -1))
        self.open_map_label.setText(QtWidgets.QApplication.translate("CosmeticWindow", "When you enter an area, the map will already be available as if the map station was used.", None, -1))
        self.pickup_markers_check.setText(QtWidgets.QApplication.translate("CosmeticWindow", "Replace Translator icons on map with item icons", None, -1))
        self.pickup_markers_label.setText(QtWidgets.QApplication.translate("CosmeticWindow", "<html><head/><body><p>Shows dots on the map (and minimap) for uncollected pickups, similar to the Corruption.</p><p>The icons <span style=\" font-weight:600;\">replace</span> the translator gate icons.</p></body></html>", None, -1))

