# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/travis/build/randovania/randovania/randovania/gui/main_rules.ui',
# licensing of '/home/travis/build/randovania/randovania/randovania/gui/main_rules.ui' applies.
#
# Created: Tue May  7 20:31:40 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainRules(object):
    def setupUi(self, MainRules):
        MainRules.setObjectName("MainRules")
        MainRules.resize(566, 705)
        MainRules.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralWidget = QtWidgets.QWidget(MainRules)
        self.centralWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scroll_area = QtWidgets.QScrollArea(self.centralWidget)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scroll_area.setLineWidth(0)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area_contents = QtWidgets.QWidget()
        self.scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 548, 687))
        self.scroll_area_contents.setObjectName("scroll_area_contents")
        self.gridLayout = QtWidgets.QGridLayout(self.scroll_area_contents)
        self.gridLayout.setObjectName("gridLayout")
        self.item_alternative_box = QtWidgets.QGroupBox(self.scroll_area_contents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.item_alternative_box.sizePolicy().hasHeightForWidth())
        self.item_alternative_box.setSizePolicy(sizePolicy)
        self.item_alternative_box.setObjectName("item_alternative_box")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.item_alternative_box)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.progressive_suit_check = QtWidgets.QCheckBox(self.item_alternative_box)
        self.progressive_suit_check.setObjectName("progressive_suit_check")
        self.verticalLayout_3.addWidget(self.progressive_suit_check)
        self.progressive_grapple_check = QtWidgets.QCheckBox(self.item_alternative_box)
        self.progressive_grapple_check.setObjectName("progressive_grapple_check")
        self.verticalLayout_3.addWidget(self.progressive_grapple_check)
        self.progressive_launcher_check = QtWidgets.QCheckBox(self.item_alternative_box)
        self.progressive_launcher_check.setObjectName("progressive_launcher_check")
        self.verticalLayout_3.addWidget(self.progressive_launcher_check)
        self.split_ammo_check = QtWidgets.QCheckBox(self.item_alternative_box)
        self.split_ammo_check.setObjectName("split_ammo_check")
        self.verticalLayout_3.addWidget(self.split_ammo_check)
        self.gridLayout.addWidget(self.item_alternative_box, 0, 0, 1, 2)
        self.random_starting_box = QtWidgets.QGroupBox(self.scroll_area_contents)
        self.random_starting_box.setObjectName("random_starting_box")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.random_starting_box)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.maximum_starting_label = QtWidgets.QLabel(self.random_starting_box)
        self.maximum_starting_label.setObjectName("maximum_starting_label")
        self.gridLayout_2.addWidget(self.maximum_starting_label, 2, 0, 1, 1)
        self.minimum_starting_label = QtWidgets.QLabel(self.random_starting_box)
        self.minimum_starting_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.minimum_starting_label.setObjectName("minimum_starting_label")
        self.gridLayout_2.addWidget(self.minimum_starting_label, 1, 0, 1, 1)
        self.minimum_starting_spinbox = QtWidgets.QSpinBox(self.random_starting_box)
        self.minimum_starting_spinbox.setMaximum(30)
        self.minimum_starting_spinbox.setObjectName("minimum_starting_spinbox")
        self.gridLayout_2.addWidget(self.minimum_starting_spinbox, 1, 1, 1, 1)
        self.random_starting_label = QtWidgets.QLabel(self.random_starting_box)
        self.random_starting_label.setWordWrap(True)
        self.random_starting_label.setObjectName("random_starting_label")
        self.gridLayout_2.addWidget(self.random_starting_label, 0, 0, 1, 2)
        self.maximum_starting_spinbox = QtWidgets.QSpinBox(self.random_starting_box)
        self.maximum_starting_spinbox.setMaximum(30)
        self.maximum_starting_spinbox.setObjectName("maximum_starting_spinbox")
        self.gridLayout_2.addWidget(self.maximum_starting_spinbox, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.random_starting_box, 1, 0, 1, 2)
        self.item_pool_box = QtWidgets.QGroupBox(self.scroll_area_contents)
        self.item_pool_box.setToolTipDuration(-1)
        self.item_pool_box.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.item_pool_box.setFlat(False)
        self.item_pool_box.setObjectName("item_pool_box")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.item_pool_box)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.ammo_box = QtWidgets.QGroupBox(self.item_pool_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ammo_box.sizePolicy().hasHeightForWidth())
        self.ammo_box.setSizePolicy(sizePolicy)
        self.ammo_box.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.ammo_box.setObjectName("ammo_box")
        self.ammo_layout = QtWidgets.QVBoxLayout(self.ammo_box)
        self.ammo_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.ammo_layout.setObjectName("ammo_layout")
        self.gridLayout_3.addWidget(self.ammo_box, 1, 1, 1, 1)
        self.major_items_box = QtWidgets.QGroupBox(self.item_pool_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.major_items_box.sizePolicy().hasHeightForWidth())
        self.major_items_box.setSizePolicy(sizePolicy)
        self.major_items_box.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.major_items_box.setObjectName("major_items_box")
        self.major_items_layout = QtWidgets.QGridLayout(self.major_items_box)
        self.major_items_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.major_items_layout.setObjectName("major_items_layout")
        self.gridLayout_3.addWidget(self.major_items_box, 1, 0, 1, 1)
        self.item_pool_count_label = QtWidgets.QLabel(self.item_pool_box)
        self.item_pool_count_label.setAlignment(QtCore.Qt.AlignCenter)
        self.item_pool_count_label.setObjectName("item_pool_count_label")
        self.gridLayout_3.addWidget(self.item_pool_count_label, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.item_pool_box, 2, 0, 1, 2)
        self.scroll_area.setWidget(self.scroll_area_contents)
        self.verticalLayout.addWidget(self.scroll_area)
        MainRules.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainRules)
        QtCore.QMetaObject.connectSlotsByName(MainRules)

    def retranslateUi(self, MainRules):
        MainRules.setWindowTitle(QtWidgets.QApplication.translate("MainRules", "Randovania", None, -1))
        self.item_alternative_box.setTitle(QtWidgets.QApplication.translate("MainRules", "Item Alternatives", None, -1))
        self.progressive_suit_check.setToolTip(QtWidgets.QApplication.translate("MainRules", "<html><head/><body><p>Instead of there being a Dark Suit and a Light Suit pickups, there will instead be two Progressive Suit pickups.</p><p>Picking the first one gives you Dark Suit, while the second one gives Light Suit. This ensures you always get Dark Suit before.</p></body></html>", None, -1))
        self.progressive_suit_check.setText(QtWidgets.QApplication.translate("MainRules", "Use progressive Dark Suit → Light Suit", None, -1))
        self.progressive_grapple_check.setToolTip(QtWidgets.QApplication.translate("MainRules", "<html><head/><body><p>This groups Grapple Beam and Screw Attack into a progressive item pair: the first one always gives Grapple Beam, with the second one always being Screw Attack.</p><p>Warning: the model for this item pair will always be Grapple Beam.</p></body></html>", None, -1))
        self.progressive_grapple_check.setText(QtWidgets.QApplication.translate("MainRules", "Use progressive Grapple Beam → Screw Attack", None, -1))
        self.progressive_launcher_check.setText(QtWidgets.QApplication.translate("MainRules", "Use progressive Missile Launcher → Seekers Launcher", None, -1))
        self.split_ammo_check.setToolTip(QtWidgets.QApplication.translate("MainRules", "<html><head/><body><p>Splits the Beam Ammo Expansion pickups into two different pickups: Light Ammo Expansion and Dark Ammo Expansion.</p></body></html>", None, -1))
        self.split_ammo_check.setText(QtWidgets.QApplication.translate("MainRules", "Split Beam Ammo Expansions", None, -1))
        self.random_starting_box.setTitle(QtWidgets.QApplication.translate("MainRules", "Random Starting Items", None, -1))
        self.maximum_starting_label.setText(QtWidgets.QApplication.translate("MainRules", "Maximum", None, -1))
        self.minimum_starting_label.setText(QtWidgets.QApplication.translate("MainRules", "Minimum", None, -1))
        self.random_starting_label.setText(QtWidgets.QApplication.translate("MainRules", "<html><head/><body><p>Randovania will add additional starting items if necessary to make the seed possible.<br/>You can enforce at least some items by increasing the minimum.<br/>The maximum causes the seed to fail instead of adding additional items.</p></body></html>", None, -1))
        self.item_pool_box.setTitle(QtWidgets.QApplication.translate("MainRules", "Item Pool", None, -1))
        self.ammo_box.setTitle(QtWidgets.QApplication.translate("MainRules", "Ammo", None, -1))
        self.major_items_box.setTitle(QtWidgets.QApplication.translate("MainRules", "Major Items", None, -1))
        self.item_pool_count_label.setToolTip(QtWidgets.QApplication.translate("MainRules", "If there are fewer than 119 items, the rest of the item locations will contain Energy Transfer Modules.", None, -1))
        self.item_pool_count_label.setText(QtWidgets.QApplication.translate("MainRules", "Items in pool: #/119", None, -1))

