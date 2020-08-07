# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\MHW-EPV-Editor\resources\SplashScreen.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 400)
        Dialog.setMinimumSize(QtCore.QSize(700, 400))
        Dialog.setMaximumSize(QtCore.QSize(700, 400))
        Dialog.setBaseSize(QtCore.QSize(700, 400))
        Dialog.setStyleSheet(" background-image:url(:/SplashImage/SplashScreen.png)")
        self.Patreon = QtWidgets.QPushButton(Dialog)
        self.Patreon.setGeometry(QtCore.QRect(0, 0, 271, 271))
        self.Patreon.setMinimumSize(QtCore.QSize(271, 271))
        self.Patreon.setMaximumSize(QtCore.QSize(271, 271))
        self.Patreon.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Patreon.setStyleSheet("border:none;")
        self.Patreon.setText("")
        self.Patreon.setObjectName("Patreon")
        self.Paypal = QtWidgets.QPushButton(Dialog)
        self.Paypal.setGeometry(QtCore.QRect(270, 280, 431, 71))
        self.Paypal.setMinimumSize(QtCore.QSize(431, 71))
        self.Paypal.setMaximumSize(QtCore.QSize(431, 71))
        self.Paypal.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Paypal.setStyleSheet("border:none;background-color: rgba(255, 255, 255, 0); background-image:url()")
        self.Paypal.setText("")
        self.Paypal.setObjectName("Paypal")
        self.Continue = QtWidgets.QPushButton(Dialog)
        self.Continue.setGeometry(QtCore.QRect(390, 360, 311, 41))
        self.Continue.setMinimumSize(QtCore.QSize(311, 41))
        self.Continue.setMaximumSize(QtCore.QSize(311, 41))
        self.Continue.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Continue.setStyleSheet("border:none;background-color: rgba(255, 255, 255, 0); background-image:url()")
        self.Continue.setText("")
        self.Continue.setObjectName("Continue")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

import resources.SplashBackground_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

