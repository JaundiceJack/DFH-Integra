# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog_NewLot.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(264, 443)
        self.acceptB = QtWidgets.QDialogButtonBox(Dialog)
        self.acceptB.setGeometry(QtCore.QRect(-90, 390, 341, 32))
        self.acceptB.setOrientation(QtCore.Qt.Horizontal)
        self.acceptB.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.acceptB.setObjectName("acceptB")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 241, 181))
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.vendorLE = QtWidgets.QLineEdit(self.groupBox)
        self.vendorLE.setObjectName("vendorLE")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.vendorLE)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.vendor_lotLE = QtWidgets.QLineEdit(self.groupBox)
        self.vendor_lotLE.setObjectName("vendor_lotLE")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.vendor_lotLE)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lot_notePT = QtWidgets.QPlainTextEdit(self.groupBox)
        self.lot_notePT.setObjectName("lot_notePT")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lot_notePT)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.item_numberLE = QtWidgets.QLineEdit(self.groupBox)
        self.item_numberLE.setEnabled(False)
        self.item_numberLE.setObjectName("item_numberLE")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.item_numberLE)
        self.lot_numberLE = QtWidgets.QLineEdit(self.groupBox)
        self.lot_numberLE.setObjectName("lot_numberLE")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lot_numberLE)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 210, 241, 81))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.amount_receivedLE = QtWidgets.QLineEdit(self.groupBox_2)
        self.amount_receivedLE.setObjectName("amount_receivedLE")
        self.gridLayout.addWidget(self.amount_receivedLE, 0, 1, 1, 1)
        self.lot_unitsCombo = QtWidgets.QComboBox(self.groupBox_2)
        self.lot_unitsCombo.setObjectName("lot_unitsCombo")
        self.lot_unitsCombo.addItem("")
        self.lot_unitsCombo.addItem("")
        self.gridLayout.addWidget(self.lot_unitsCombo, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.receiving_poLE = QtWidgets.QLineEdit(self.groupBox_2)
        self.receiving_poLE.setObjectName("receiving_poLE")
        self.gridLayout.addWidget(self.receiving_poLE, 1, 1, 1, 1)
        self.groupBox_22 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_22.setGeometry(QtCore.QRect(10, 300, 241, 82))
        self.groupBox_22.setObjectName("groupBox_22")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_22)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_27 = QtWidgets.QLabel(self.groupBox_22)
        self.label_27.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_27.setObjectName("label_27")
        self.gridLayout_2.addWidget(self.label_27, 0, 0, 1, 1)
        self.facilityCombo = QtWidgets.QComboBox(self.groupBox_22)
        self.facilityCombo.setObjectName("facilityCombo")
        self.facilityCombo.addItem("")
        self.facilityCombo.addItem("")
        self.facilityCombo.addItem("")
        self.facilityCombo.addItem("")
        self.gridLayout_2.addWidget(self.facilityCombo, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(88, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.groupBox_22)
        self.label_29.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_29.setObjectName("label_29")
        self.gridLayout_2.addWidget(self.label_29, 1, 0, 1, 1)
        self.wh_codeLE = QtWidgets.QLineEdit(self.groupBox_22)
        self.wh_codeLE.setObjectName("wh_codeLE")
        self.gridLayout_2.addWidget(self.wh_codeLE, 1, 1, 1, 2)

        self.retranslateUi(Dialog)
        self.acceptB.accepted.connect(Dialog.accept)
        self.acceptB.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.item_numberLE, self.lot_numberLE)
        Dialog.setTabOrder(self.lot_numberLE, self.vendorLE)
        Dialog.setTabOrder(self.vendorLE, self.vendor_lotLE)
        Dialog.setTabOrder(self.vendor_lotLE, self.lot_notePT)
        Dialog.setTabOrder(self.lot_notePT, self.amount_receivedLE)
        Dialog.setTabOrder(self.amount_receivedLE, self.lot_unitsCombo)
        Dialog.setTabOrder(self.lot_unitsCombo, self.receiving_poLE)
        Dialog.setTabOrder(self.receiving_poLE, self.facilityCombo)
        Dialog.setTabOrder(self.facilityCombo, self.wh_codeLE)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "Basic Info"))
        self.label.setText(_translate("Dialog", "Vendor:"))
        self.label_2.setText(_translate("Dialog", "Vendor Lot:"))
        self.label_3.setText(_translate("Dialog", "Lot notes:"))
        self.label_6.setText(_translate("Dialog", "Item Number:"))
        self.label_7.setText(_translate("Dialog", "Lot Number:"))
        self.groupBox_2.setTitle(_translate("Dialog", "Receiving"))
        self.label_4.setText(_translate("Dialog", "Amount Received:"))
        self.lot_unitsCombo.setItemText(0, _translate("Dialog", "kg"))
        self.lot_unitsCombo.setItemText(1, _translate("Dialog", "ths"))
        self.label_5.setText(_translate("Dialog", "Receiving PO:"))
        self.groupBox_22.setTitle(_translate("Dialog", "Location"))
        self.label_27.setText(_translate("Dialog", "Facility:"))
        self.facilityCombo.setItemText(0, _translate("Dialog", "AMM"))
        self.facilityCombo.setItemText(1, _translate("Dialog", "LVN"))
        self.facilityCombo.setItemText(2, _translate("Dialog", "CT"))
        self.facilityCombo.setItemText(3, _translate("Dialog", "FL"))
        self.label_29.setText(_translate("Dialog", "WH Code:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

