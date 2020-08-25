# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 15:03:21 2020

@author: AsteriskAmpersand
"""

from UVSManagerGUI import Ui_MainWindow
from UVS import UVSFile,compileSpacings,UVSCompile
from UVGroup import UVGroup
from splash.Splash import SplashScreen

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication,QFileDialog,QListWidgetItem,QShortcut
from PyQt5.QtGui import QKeySequence, QPalette, QColor, QDesktopServices,QIcon

import os

class UVSManager(QtWidgets.QMainWindow):
    saveInto = pyqtSignal(object,int,int)
    def __init__(self, parent = None):
        super().__init__(parent)

        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        elif __file__:
            application_path = os.path.dirname(__file__)
        self.setWindowIcon(QIcon(application_path+r"\resources\DodoSama.png"))
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("UltraViolet - UVS Editor")
        self.connect()
        self.currentFile = None        
        self.show()
        
    def open(self):
        uvs = QFileDialog.getOpenFileName(self, "Open UVS", "", "MHW UVS File (*.uvs)")[0]
        if uvs:
            try:
                with open(uvs,"rb") as uvf:
                    uvs_data = UVSFile.parse(uvf.read())
                    self.marshall(uvs_data)
                    self.currentFile = uvs
            except:
                return
            self.currentFile = uvs
    
    def marshall(self,uvs):
        self.ui.pathWidget.clear()
        for group in uvs.Groups:
            pindex = group.mapIndices[:group.mapCount] if group.mapCount else []
            tString = [uvs.Strings[p] for p in pindex]
            tpaths = [s.string for s in tString]
            ttypes = [s.type for s in tString]
            dynamic = group.unkn3
            framedata = [(tuple(frame.uv0),tuple(frame.uv1))
                            for frame in group.frameData]
            litem = UVGroup('\n'.join(tpaths),framedata,tpaths,ttypes,dynamic)
            self.ui.pathWidget.addItem(litem)
    
    def connect(self):
        widget = self.ui.pathWidget
        self.ui.actionNew.triggered.connect(self.new)
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSave_As.triggered.connect(self.saveAs)
        self.ui.browse.pressed.connect(self.browseChunk)
        
    def browseChunk(self):
        chunk = QFileDialog.getExistingDirectory(self, "Open Chunk Root", "")
        if chunk:
            self.ui.root.setText(chunk)
    
    def hotkeys(self):
        #delete
        self.delete = QShortcut(QKeySequence("Del"), self)
        self.delete.activated.connect(self.ui.pathWidget.delete)
    
    def new(self):
        self.currentFile = None
        self.ui.pathWidget.clear()
    
    def save(self):
        if self.currentFile is None:
            self.saveAs()
        else:
            self.__save__(self.currentFile)
            self.currentFile = self.currentFile
            
    def saveAs(self):
        saveFile =  QFileDialog.getSaveFileName(self, "Save UVS", "", "MHW UVS File (*.uvs)")[0]
        if saveFile:
            self.__save__(saveFile)            
        
    def __save__(self,path): 
        serialData = self.serialize()
        with open(path,"wb") as inf:
            inf.write(serialData)

    def serialize(self):
        groups = self.ui.pathWidget
        paths = list(dict.fromkeys([(path,typing) 
                                        for group in self.ui.pathWidget 
                                        for path,typing in zip(group.paths,group.types)
                                    ]))
        for group in groups:
            group.indexize(paths)
        (groupOffset,groupCount,stringOffset,stringCount,
        frameDataOffsets,frameDataCounts,indexOffsets,frameDataCounts,mapIndexOffset,
        stringOffsets) = compileSpacings(groups,paths)
        Header = {"uvsSignature":b"UVS\x00","ibSignature":[0,7,18,22],
                  "groupOffset":groupOffset,"groupCount":groupCount,
                  "stringOffset":stringOffset,"stringCount":stringCount}
        GroupHeaders = [{"frameDataOffset":fdOffset,"frameCount":fCount,
                         "frameIndexOffset":fiOffset,"frameIndexCount":fCount,
                         "dataOffset":dOffset,"mapCount":len(group.types),
                         "unkn32_0":32,"unkn32_1":32,"unkn3":group.dynamic} 
                        for group,fdOffset,fCount,fiOffset,dOffset in 
                        zip(groups,frameDataOffsets,frameDataCounts,indexOffsets,mapIndexOffset)]
        groupPad = lambda x: x + [0]*((-len(x))%4)
        GroupBlocks = [(  [{"uv0":uv0,"uv1":uv1,"unkn":[.5,.5,0,0]} for uv0,uv1 in group.framedata],
                          {"frameIndices":list(range(len(group.framedata)))},
                          {"mapIndices":groupPad(group.indices) if len(group.framedata) else []})                        
                        for group in groups]
        StringBlocks = [{"blank":0,"stringOffset":offset,"type":typing} 
                            for offset,(string,typing) in zip(stringOffsets,paths)]
        StringData = [{"string":string} for string,typing in paths]
        binaryUVS = UVSCompile(Header,GroupHeaders,GroupBlocks,StringBlocks,StringData)
        return binaryUVS

# =============================================================================
# Dark Theming
# =============================================================================

def setStyle(app):
    from PyQt5.QtCore import Qt
    app.setStyle("Fusion")
    darkPalette = QPalette()
    darkPalette.setColor(QPalette.Window,QColor(53,53,53));
    darkPalette.setColor(QPalette.WindowText,Qt.white);
    darkPalette.setColor(QPalette.Disabled,QPalette.WindowText,QColor(127,127,127));
    darkPalette.setColor(QPalette.Base,QColor(42,42,42));
    darkPalette.setColor(QPalette.AlternateBase,QColor(66,66,66));
    darkPalette.setColor(QPalette.ToolTipBase,Qt.white);
    darkPalette.setColor(QPalette.ToolTipText,Qt.white);
    darkPalette.setColor(QPalette.Text,Qt.white);
    darkPalette.setColor(QPalette.Disabled,QPalette.Text,QColor(127,127,127));
    darkPalette.setColor(QPalette.Dark,QColor(35,35,35));
    darkPalette.setColor(QPalette.Shadow,QColor(20,20,20));
    darkPalette.setColor(QPalette.Button,QColor(53,53,53));
    darkPalette.setColor(QPalette.ButtonText,Qt.white);
    darkPalette.setColor(QPalette.Disabled,QPalette.ButtonText,QColor(127,127,127));
    darkPalette.setColor(QPalette.BrightText,Qt.red);
    darkPalette.setColor(QPalette.Link,QColor(42,130,218));
    darkPalette.setColor(QPalette.Highlight,QColor(42,130,218));
    darkPalette.setColor(QPalette.Disabled,QPalette.Highlight,QColor(80,80,80));
    darkPalette.setColor(QPalette.HighlightedText,Qt.white);
    darkPalette.setColor(QPalette.Disabled,QPalette.HighlightedText,QColor(127,127,127));
    app.setPalette(darkPalette)

if "__main__" in __name__:
    import sys
    app = QApplication(sys.argv)
    args = app.arguments()[1:]
    splash = SplashScreen()
    response = splash.exec()
    
    if not response:
        sys.exit(app.exec_())
        
    #app = QApplication(sys.argv)
    setStyle(app)
    window = UVSManager()
    sys.exit(app.exec_())
