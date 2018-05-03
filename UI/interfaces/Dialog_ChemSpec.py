# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog_ChemSpec.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(274, 208)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.is_chem_nameLE = QtWidgets.QLineEdit(self.groupBox)
        self.is_chem_nameLE.setEnabled(False)
        self.is_chem_nameLE.setObjectName("is_chem_nameLE")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.is_chem_nameLE)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.is_methodCombo = QtWidgets.QComboBox(self.groupBox)
        self.is_methodCombo.setObjectName("is_methodCombo")
        self.is_methodCombo.addItem("")
        self.is_methodCombo.addItem("")
        self.is_methodCombo.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.is_methodCombo)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.is_presenceCombo = QtWidgets.QComboBox(self.groupBox)
        self.is_presenceCombo.setObjectName("is_presenceCombo")
        self.is_presenceCombo.addItem("")
        self.is_presenceCombo.addItem("")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.is_presenceCombo)
        self.is_chem_nameCombo = QtWidgets.QComboBox(self.groupBox)
        self.is_chem_nameCombo.setObjectName("is_chem_nameCombo")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.is_chem_nameCombo)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
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
        Dialog.setTabOrder(self.is_chem_nameLE, self.is_methodCombo)
        Dialog.setTabOrder(self.is_methodCombo, self.is_presenceCombo)
        Dialog.setTabOrder(self.is_presenceCombo, self.is_chem_nameCombo)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "Chemical Identification Specifications"))
        self.label_2.setText(_translate("Dialog", "Detection Method:"))
        self.is_methodCombo.setItemText(0, _translate("Dialog", "HPLC"))
        self.is_methodCombo.setItemText(1, _translate("Dialog", "UV-Vis"))
        self.is_methodCombo.setItemText(2, _translate("Dialog", "ICP-OES"))
        self.label_3.setText(_translate("Dialog", "Presence:"))
        self.is_presenceCombo.setItemText(0, _translate("Dialog", "Positive"))
        self.is_presenceCombo.setItemText(1, _translate("Dialog", "Negative"))
        self.label.setText(_translate("Dialog", "Chemical Name:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

