# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 03:55:47 2020

@author: AsteriskAmpersand
"""

from ImageDialogGUI import Ui_Dialog
from UVGroup import UVGroup

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog,QFileDialog

from collections import OrderedDict
#from PyQt5.QtCore import QFile, QTextStream

from pathlib import Path

class ImageDialog(QDialog):
    def __init__(self, *args):
        super().__init__(*args)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Add File")
        self.animatable = True
        
        self.connect()
        self.setModal(True)
        #self.show()
        
    def populate(self,group):
        self.animatable = False
        self.framedata = group.framedata
        paths = [self.ui.Path0,self.ui.Path1,self.ui.Path2,self.ui.Path3]
        types = [self.ui.Type0,self.ui.Type1,self.ui.Type2,self.ui.Type3]
        for path,target in zip(group.paths,paths):
            target.setText(path)
        for typing,target in zip(group.types,types):
            target.setCurrentIndex(typing-1)
        self.ui.Unkn3.setValue(group.dynamic)
        self.disable()
    
    def disable(self):
        self.ui.Animated.setEnabled(False)
    
    def connect(self):
        self.ui.OK.pressed.connect(self.accept)
        self.ui.Cancel.pressed.connect(self.reject)
        self.ui.Open.pressed.connect(self.openCSV)
        self.ui.OpenFile0.pressed.connect(self.metaOpenFile(0))
        self.ui.OpenFile1.pressed.connect(self.metaOpenFile(1))
        self.ui.OpenFile2.pressed.connect(self.metaOpenFile(2))
        self.ui.OpenFile3.pressed.connect(self.metaOpenFile(3))
        animData = self.ui.AnimationData
        animData.setEnabled(False)
        self.ui.Animated.clicked.connect(lambda: animData.setEnabled(not animData.isEnabled()))
        
    def openCSV(self):
        csvf = QFileDialog.getOpenFileName(self, "Open CSV", "", "Comma Separated Values (*.csv)")[0]
        if csvf:
            self.ui.CSV.setText(csvf)
    
    def metaOpenFile(self,index):
        def openFile():
            tex = QFileDialog.getOpenFileName(self, "Open Tex", "", "MHW Tex File (*.tex)")[0]
            if tex:
                tex = str(Path(tex).with_suffix(''))
                root = self.parent().parent().parent().ui.root.text()
                if root:
                    try:
                        tex=str(Path(tex).relative_to(root))
                    except:
                        pass
                getattr(self.ui,"Path%d"%index).setText(tex)
        return openFile
    
    def openFile(self):
        tex = QFileDialog.getOpenFileName(self, "Open Tex", "", "MHW Tex File (*.tex)")[0]
        if tex:
            self.ui.Path.setText(tex)
    
    def compileFrames(self):
        if self.ui.Animated.isChecked():
            s = self.ui
            udlr,udrl,dulr,durl = s.UDLR.isChecked(),s.UDRL.isChecked(),s.DULR.isChecked(),s.DURL.isChecked()
            lrud,rlud,lrdu,rldu = s.LRUD.isChecked(),s.RLUD.isChecked(),s.LRDU.isChecked(),s.RLDU.isChecked()
            if s.Horizontal.value() and s.Vertical.value():
                w,h = 1/s.Horizontal.value(),1/s.Vertical.value()
                framedata = [
                        ((i*w,j*h),((i+1)*w,(j+1)*h))
                        for i in range(s.Horizontal.value()) for j in range(s.Vertical.value())
                        ]
            else:
                framedata = []
            if s.Custom.isChecked():
                framedata = self.parseCSV(s.CSV.text())
            else:
                def idem(arg):return arg
                def rev(arg):return tuple(reversed(arg))
                if udlr or udrl or dulr or durl: f = idem
                else: f = rev
                iSg = udlr + dulr + lrud + lrdu + -1*(udrl + durl + rlud + rldu)
                jSg = udlr + udrl + lrud + rldu + -1*(dulr + durl + rlud + lrdu)
                signum = lambda uv: (iSg*uv[0],jSg*uv[1])
                frameCount = max(0,min(len(framedata),self.ui.FrameCount.value()))
                framedata = list(sorted(framedata,key = lambda p: f(signum(p[0])) ))[:frameCount]
        else:
            framedata = [((0,0),(1,1))]
        return framedata
    
    def fetchFrames(self):
        return self.framedata
    
    def compile(self):
        if self.animatable:
            framedata = self.compileFrames()
        else:
            framedata = self.fetchFrames()
        #there can be more than one path and litem accepts \n
        paths = [self.ui.Path0,self.ui.Path1,self.ui.Path2,self.ui.Path3]
        types = [self.ui.Type0,self.ui.Type1,self.ui.Type2,self.ui.Type3]
        pathtype = list(zip(paths,types))
        name = '\n'.join([p.text() for p,t in pathtype if p.text()])
        tpaths = [p.text() for p,t in pathtype if p.text()]
        ttypes = [t.currentIndex()+1 for p,t in pathtype if p.text()]
        dynamic = self.ui.Unkn3.value()
        litem = UVGroup(name,framedata,tpaths,ttypes,dynamic)
        return litem
    
    def parseCSV(self,path):
        with open(path,"r") as inf:
            return [tuple(line.replace("\n","").replace("\r","").split(",")) for line in inf]