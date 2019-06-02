# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Project/UicCompilerOptionsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UicCompilerOptionsDialog(object):
    def setupUi(self, UicCompilerOptionsDialog):
        UicCompilerOptionsDialog.setObjectName("UicCompilerOptionsDialog")
        UicCompilerOptionsDialog.resize(500, 246)
        UicCompilerOptionsDialog.setSizeGripEnabled(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(UicCompilerOptionsDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.packageGroup = QtWidgets.QGroupBox(UicCompilerOptionsDialog)
        self.packageGroup.setObjectName("packageGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.packageGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.packageEdit = E5ClearableLineEdit(self.packageGroup)
        self.packageEdit.setObjectName("packageEdit")
        self.verticalLayout_2.addWidget(self.packageEdit)
        self.label_2 = QtWidgets.QLabel(self.packageGroup)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.verticalLayout_3.addWidget(self.packageGroup)
        self.suffixGroup = QtWidgets.QGroupBox(UicCompilerOptionsDialog)
        self.suffixGroup.setObjectName("suffixGroup")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.suffixGroup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.suffixEdit = E5ClearableLineEdit(self.suffixGroup)
        self.suffixEdit.setObjectName("suffixEdit")
        self.verticalLayout.addWidget(self.suffixEdit)
        self.label_4 = QtWidgets.QLabel(self.suffixGroup)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.verticalLayout_3.addWidget(self.suffixGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(UicCompilerOptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(UicCompilerOptionsDialog)
        self.buttonBox.accepted.connect(UicCompilerOptionsDialog.accept)
        self.buttonBox.rejected.connect(UicCompilerOptionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UicCompilerOptionsDialog)
        UicCompilerOptionsDialog.setTabOrder(self.packageEdit, self.suffixEdit)

    def retranslateUi(self, UicCompilerOptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        UicCompilerOptionsDialog.setWindowTitle(_translate("UicCompilerOptionsDialog", "uic Compiler Options"))
        self.packageGroup.setTitle(_translate("UicCompilerOptionsDialog", "\'import\' Package"))
        self.packageEdit.setToolTip(_translate("UicCompilerOptionsDialog", "Enter the package name"))
        self.label_2.setText(_translate("UicCompilerOptionsDialog", "<b>Note</b>: This generates statements like \'from PACKAGE import ...\'."))
        self.suffixGroup.setTitle(_translate("UicCompilerOptionsDialog", "Resources Suffix"))
        self.suffixEdit.setToolTip(_translate("UicCompilerOptionsDialog", "Enter the suffix of compiled resource files (default: _rc)"))
        self.label_4.setText(_translate("UicCompilerOptionsDialog", "<b>Note</b>: Leave the suffix empty to use the default of \'_rc\'."))


from E5Gui.E5LineEdit import E5ClearableLineEdit
