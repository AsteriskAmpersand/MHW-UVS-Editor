# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 01:19:28 2020

@author: AsteriskAmpersand
"""
from PathManagerGUI import Ui_Form

from PyQt5 import QtWidgets
from ImageDialog import ImageDialog
from PyQt5.QtCore import pyqtSignal
#from PyQt5.QtWidgets import QFileDialog, QApplication,QAction,QMenu
#from PyQt5.QtCore import QModelIndex, pyqtSignal, Qt, QCoreApplication

class PathManager(QtWidgets.QWidget):
    saveInto = pyqtSignal(object,int,int)
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.connect()
        self.show()
        
    def connect(self):
        ui = self.ui
        ui.Up.pressed.connect(self.moveUp)
        ui.Down.pressed.connect(self.moveDown)
        ui.Add.pressed.connect(self.add)
        ui.Delete.pressed.connect(self.delete)
        ui.Clear.pressed.connect(self.clear)
        ui.paths.itemDoubleClicked.connect(self.edit)
    
    def clear(self):
        self.ui.paths.clear()
    
    def edit(self):
        dialog = ImageDialog(self)
        group = self.ui.paths.currentItem()
        if not group:
            return
        dialog.populate(group)
        dialog.exec()
        if dialog.result():
            item = dialog.compile()
            group.setText(item.text())
            for itemVar in ["framedata","paths","types","dynamic"]:
                setattr(group,itemVar,getattr(item,itemVar))
            #self.ui.paths.setCurrentItem(item)
        
    
    def add(self):
        dialog = ImageDialog(self)
        dialog.exec()
        if dialog.result():
            item = dialog.compile()
            self.addItem(item)
        return dialog.result()
    
    def addItem(self,item):
        self.ui.paths.addItem(item)
    
    def delete(self):
        paths = self.ui.paths
        if paths.currentRow() == -1:
            # no selection. delete last row
            row_num = paths.count() - 1
        else:
            row_num = paths.currentRow()
        item = paths.takeItem(row_num)
        del item
    
    def moveUp(self):
        paths = self.ui.paths
        row_num = paths.currentRow()
        if row_num > 0:            
            row = paths.itemWidget(paths.currentItem())
            itemN = paths.currentItem().clone()
            paths.insertItem(row_num -1, itemN)
            paths.setItemWidget(itemN, row)
            paths.takeItem(row_num+1)
            paths.setCurrentRow(row_num-1)
    
    def moveDown(self):
        paths = self.ui.paths
        row_num = paths.currentRow()
        if row_num == -1:
            # no selection. abort
            return
        elif row_num < paths.count()-1:
            row = paths.itemWidget(paths.currentItem())
            itemN = paths.currentItem().clone()
            paths.insertItem(row_num + 2, itemN)
            paths.setItemWidget(itemN, row)
            paths.takeItem(row_num)
            paths.setCurrentRow(row_num+1)
            
    def __iter__(self):
        return iter((self.ui.paths.item(i) for i in range(self.ui.paths.count())))
    
    def __len__(self):
        return self.ui.paths.count()

if "__main__" in __name__:
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = PathManager()
    sys.exit(app.exec_())