# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PathManagerGUI.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(679, 286)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.paths = QtWidgets.QListWidget(Form)
        self.paths.setObjectName("paths")
        self.horizontalLayout.addWidget(self.paths)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setMinimumSize(QtCore.QSize(159, 238))
        self.frame.setMaximumSize(QtCore.QSize(178, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.Up = QtWidgets.QPushButton(self.frame)
        self.Up.setObjectName("Up")
        self.verticalLayout.addWidget(self.Up)
        self.Add = QtWidgets.QPushButton(self.frame)
        self.Add.setObjectName("Add")
        self.verticalLayout.addWidget(self.Add)
        self.Delete = QtWidgets.QPushButton(self.frame)
        self.Delete.setObjectName("Delete")
        self.verticalLayout.addWidget(self.Delete)
        self.Clear = QtWidgets.QPushButton(self.frame)
        self.Clear.setObjectName("Clear")
        self.verticalLayout.addWidget(self.Clear)
        self.Down = QtWidgets.QPushButton(self.frame)
        self.Down.setObjectName("Down")
        self.verticalLayout.addWidget(self.Down)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Up.setText(_translate("Form", "^"))
        self.Add.setText(_translate("Form", "Add"))
        self.Delete.setText(_translate("Form", "Delete"))
        self.Clear.setText(_translate("Form", "Clear"))
        self.Down.setText(_translate("Form", "v"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

