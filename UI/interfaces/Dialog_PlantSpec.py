# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog_PlantSpec.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(305, 204)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.is_genusLE = QtWidgets.QLineEdit(self.groupBox)
        self.is_genusLE.setObjectName("is_genusLE")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.is_genusLE)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.is_speciesLE = QtWidgets.QLineEdit(self.groupBox)
        self.is_speciesLE.setObjectName("is_speciesLE")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.is_speciesLE)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.is_partLE = QtWidgets.QLineEdit(self.groupBox)
        self.is_partLE.setObjectName("is_partLE")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.is_partLE)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.is_solventCombo = QtWidgets.QComboBox(self.groupBox)
        self.is_solventCombo.setObjectName("is_solventCombo")
        self.is_solventCombo.addItem("")
        self.is_solventCombo.addItem("")
        self.is_solventCombo.addItem("")
        self.is_solventCombo.addItem("")
        self.is_solventCombo.addItem("")
        self.is_solventCombo.addItem("")
        self.is_solventCombo.addItem("")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.is_solventCombo)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.is_methodCombo = QtWidgets.QComboBox(self.groupBox)
        self.is_methodCombo.setObjectName("is_methodCombo")
        self.is_methodCombo.addItem("")
        self.is_methodCombo.addItem("")
        self.is_methodCombo.addItem("")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.is_methodCombo)
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
        Dialog.setTabOrder(self.is_genusLE, self.is_speciesLE)
        Dialog.setTabOrder(self.is_speciesLE, self.is_partLE)
        Dialog.setTabOrder(self.is_partLE, self.is_solventCombo)
        Dialog.setTabOrder(self.is_solventCombo, self.is_methodCombo)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "Botanical Identification Specification"))
        self.label.setText(_translate("Dialog", "Genus:"))
        self.label_2.setText(_translate("Dialog", "Species:"))
        self.label_4.setText(_translate("Dialog", "Plant Part:"))
        self.label_5.setText(_translate("Dialog", "Extraction Solvent:"))
        self.is_solventCombo.setItemText(0, _translate("Dialog", "Water"))
        self.is_solventCombo.setItemText(1, _translate("Dialog", "Ethanol"))
        self.is_solventCombo.setItemText(2, _translate("Dialog", "Ethanol & Water"))
        self.is_solventCombo.setItemText(3, _translate("Dialog", "Methanol"))
        self.is_solventCombo.setItemText(4, _translate("Dialog", "Methanol & Water"))
        self.is_solventCombo.setItemText(5, _translate("Dialog", "Toluene"))
        self.is_solventCombo.setItemText(6, _translate("Dialog", "Other"))
        self.label_3.setText(_translate("Dialog", "ID Method:"))
        self.is_methodCombo.setItemText(0, _translate("Dialog", "HPTLC"))
        self.is_methodCombo.setItemText(1, _translate("Dialog", "HPLC"))
        self.is_methodCombo.setItemText(2, _translate("Dialog", "Other"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

