# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog_HMSpec.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(299, 204)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.is_unitCombo = QtWidgets.QComboBox(self.groupBox)
        self.is_unitCombo.setObjectName("is_unitCombo")
        self.is_unitCombo.addItem("")
        self.is_unitCombo.addItem("")
        self.is_unitCombo.addItem("")
        self.is_unitCombo.addItem("")
        self.is_unitCombo.addItem("")
        self.gridLayout.addWidget(self.is_unitCombo, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.is_asLE = QtWidgets.QLineEdit(self.groupBox)
        self.is_asLE.setObjectName("is_asLE")
        self.gridLayout.addWidget(self.is_asLE, 1, 1, 1, 1)
        self.is_unitL1 = QtWidgets.QLabel(self.groupBox)
        self.is_unitL1.setObjectName("is_unitL1")
        self.gridLayout.addWidget(self.is_unitL1, 1, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.is_cdLE = QtWidgets.QLineEdit(self.groupBox)
        self.is_cdLE.setObjectName("is_cdLE")
        self.gridLayout.addWidget(self.is_cdLE, 2, 1, 1, 1)
        self.is_unitL2 = QtWidgets.QLabel(self.groupBox)
        self.is_unitL2.setObjectName("is_unitL2")
        self.gridLayout.addWidget(self.is_unitL2, 2, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.is_pbLE = QtWidgets.QLineEdit(self.groupBox)
        self.is_pbLE.setObjectName("is_pbLE")
        self.gridLayout.addWidget(self.is_pbLE, 3, 1, 1, 1)
        self.is_unitL3 = QtWidgets.QLabel(self.groupBox)
        self.is_unitL3.setObjectName("is_unitL3")
        self.gridLayout.addWidget(self.is_unitL3, 3, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.is_hgLE = QtWidgets.QLineEdit(self.groupBox)
        self.is_hgLE.setObjectName("is_hgLE")
        self.gridLayout.addWidget(self.is_hgLE, 4, 1, 1, 1)
        self.is_unitL4 = QtWidgets.QLabel(self.groupBox)
        self.is_unitL4.setObjectName("is_unitL4")
        self.gridLayout.addWidget(self.is_unitL4, 4, 2, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.acceptB = QtWidgets.QDialogButtonBox(Dialog)
        self.acceptB.setOrientation(QtCore.Qt.Horizontal)
        self.acceptB.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.acceptB.setObjectName("acceptB")
        self.gridLayout_2.addWidget(self.acceptB, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.acceptB.accepted.connect(Dialog.accept)
        self.acceptB.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.is_unitCombo, self.is_asLE)
        Dialog.setTabOrder(self.is_asLE, self.is_cdLE)
        Dialog.setTabOrder(self.is_cdLE, self.is_pbLE)
        Dialog.setTabOrder(self.is_pbLE, self.is_hgLE)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "Heavy Metal Specifications"))
        self.label_5.setText(_translate("Dialog", "Units:"))
        self.is_unitCombo.setItemText(0, _translate("Dialog", "ppm"))
        self.is_unitCombo.setItemText(1, _translate("Dialog", "mcg/serving"))
        self.is_unitCombo.setItemText(2, _translate("Dialog", "mcg/sg"))
        self.is_unitCombo.setItemText(3, _translate("Dialog", "mcg/tablet"))
        self.is_unitCombo.setItemText(4, _translate("Dialog", "mcg/capsule"))
        self.label.setText(_translate("Dialog", "Arsenic less than:"))
        self.is_unitL1.setText(_translate("Dialog", "ppm"))
        self.label_2.setText(_translate("Dialog", "Cadmium less than:"))
        self.is_unitL2.setText(_translate("Dialog", "ppm"))
        self.label_3.setText(_translate("Dialog", "Lead less than:"))
        self.is_unitL3.setText(_translate("Dialog", "ppm"))
        self.label_4.setText(_translate("Dialog", "Mercury less than:"))
        self.is_unitL4.setText(_translate("Dialog", "ppm"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

