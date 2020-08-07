# -*- coding: utf-8 -*-
"""
Created on Wed May  6 11:43:21 2020

@author: AsteriskAmpersand
"""

import sys
import io
import html
import contextlib
from PyQt5.QtWidgets import QDialog,QApplication,QShortcut
from PyQt5.QtGui import QTextCursor,QKeySequence,QFont,QFontMetrics
from gui.InteractiveConsole import Ui_Dialog


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = io.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

OpenHtml = "<font>";
ErrorHtml = "<font color=\"Red\">";
OutputHtml = "<font color=\"DarkOrange\">";
EndHtml = "</font>" #<br>

escape = lambda x: html.escape(x).replace("\n","<br>").replace("\t","&nbsp;&nbsp;&nbsp;&nbsp;")

Error = lambda y: "%s%s%s"%(ErrorHtml,escape(str(y)),EndHtml)
Output = lambda y: "%s%s%s"%(OutputHtml,escape(str(y)),EndHtml)
Input = lambda y: "%s%s%s"%(OpenHtml,escape(">> "+ str(y).replace("\n","\n>> ")),EndHtml)

class InteractiveConsole(QDialog):
    def __init__(self, localVars=None, *args):
        if localVars is None:
            localVars = {}
        super().__init__(*args)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Interactive Python Console")
        
        self.setFormating()
        
        self.locals = localVars
        self.actionParse = QShortcut(QKeySequence("Ctrl+Return"),self)
        self.actionParse.activated.connect(self.getInput)
        #self.connectSignals()
        #self.setDelegates()
        self.show()
        
    def setFormating(self):
        for editor in [self.ui.Input,self.ui.Output]:
            font = QFont()
            font.setFamily("Courier")
            font.setStyleHint(QFont.Monospace)
            font.setFixedPitch(True)
            font.setPointSize(10)
            
            editor.setFont(font)
            tabStop = 4
    
            metrics = QFontMetrics(font)
            editor.setTabStopWidth(tabStop * metrics.width(' '))
        
    def getInput(self):
        text = self.ui.Input.document().toPlainText()
        try:
            with stdoutIO() as results:
                exec(text,{},self.locals)
            self.displayOutput(text,results.getvalue())
        except Exception as error:
            #print(error)
            #raise error
            self.displayError(text,str(error.with_traceback(error.__traceback__))+"\n")
        self.ui.Input.setText("")
        

    def displayOutput(self,textInput,textOutput):
        self.display(Input(textInput))
        self.display(Output(textOutput))
    def displayError(self,textInput,errorOutput):
        self.display(Input(textInput))
        self.display(Error(errorOutput))
    def display(self,text):
        #cursor = self.ui.Output.message.textCursor()
        #cursor = self.ui.Output.textCursor()
        #if(not cursor.atStart()):
        #    cursor.insertBlock()
        self.ui.Output.append(text)
        self.ui.Output.verticalScrollBar().setValue(self.ui.Output.verticalScrollBar().maximum())
        #cursor.movePosition(QTextCursor.End);
        #self.ui.Output.setTextCursor(cursor);
    

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Dialog = InteractiveConsole()
    Dialog.show()
    sys.exit(app.exec_())
