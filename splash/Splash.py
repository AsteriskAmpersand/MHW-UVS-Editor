import sys
import os

from resources.SplashScreen import Ui_Dialog

#from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import Qt,QUrl
#from PyQt5.QtCore import QFile, QTextStream

class SplashScreen(QDialog):
    def __init__(self, *args):
        super().__init__(*args)
#        self.setWindowIcon(QtGui.QIcon(application_path+r"\resources\DodoSama.png"))
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.connectSignals()
        
        self.show()
        
    def connectSignals(self):
        self.ui.Patreon.pressed.connect(self.toPatreon)
        self.ui.Paypal.pressed.connect(self.toPaypal)
        self.ui.Continue.pressed.connect(self.accept)
    def toPaypal(self):
        QDesktopServices.openUrl(QUrl("https://www.paypal.me/AsteriskAmpersand?locale.x=en_US"))
    def toPatreon(self):
        QDesktopServices.openUrl(QUrl("https://www.patreon.com/user?u=21034864&fan_landing=true"))

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = SplashScreen()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())