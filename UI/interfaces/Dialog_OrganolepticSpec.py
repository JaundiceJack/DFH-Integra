# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog_OrganolepticSpec.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(302, 152)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.is_colorLE = QtWidgets.QLineEdit(self.groupBox)
        self.is_colorLE.setObjectName("is_colorLE")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.is_colorLE)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.is_odorLE = QtWidgets.QLineEdit(self.groupBox)
        self.is_odorLE.setObjectName("is_odorLE")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.is_odorLE)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.is_appearanceLE = QtWidgets.QLineEdit(self.groupBox)
        self.is_appearanceLE.setObjectName("is_appearanceLE")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.is_appearanceLE)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.acceptB = QtWidgets.QDialogButtonBox(Dialog)
        self.acceptB.setOrientation(QtCore.Qt.Horizontal)
        self.acceptB.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.acceptB.setObjectName("acceptB")
        self.gridLayout.addWidget(self.acceptB, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.acceptB.accepted.connect(Dialog.accept)
        self.acceptB.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "Organoleptic Specifications"))
        self.label.setText(_translate("Dialog", "Color:"))
        self.label_2.setText(_translate("Dialog", "Odor:"))
        self.label_3.setText(_translate("Dialog", "Appearance:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

