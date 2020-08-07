# -*- coding: utf-8 -*-
"""
Created on Sat May  2 03:12:05 2020

@author: AsteriskAmpersand
"""

from PyQt5.QtCore import QAbstractListModel,QModelIndex,Qt,QVariant
from generic.UndoRedoController import InvertingUndoRedoController

from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView,QMessageBox

"""
import sys
def catch_exceptions(t, val, tb):
    QMessageBox.critical(None,
                       "An exception was raised",
                       "Exception type: {}".format(tb))
    old_hook(t, val, tb)


old_hook = sys.excepthook
sys.excepthook = catch_exceptions
"""

def iterable(ob):
    try:
        iter(ob)
        return True
    except:
        return False

class NoneObject():
    def __bool__(self):
        return False
    def getRole(self,role):
        return None

class QList(QAbstractListModel):
    supportedBuiltins = [int,bool,str,float]
    
    def __init__(self,iterable=None,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if iterable is None:
            iterable = []
        self.list = iterable
        self.undoer = InvertingUndoRedoController()
        
    def assign(self,index,data):
        ix = index.row()
        self.undoer.recordEvent(self.assign,(index,self.list[ix]))
        self.list[ix] = data
        self.dataChanged.emit(index,index)
        return True
        
    def setData(self,index,value,role=Qt.EditRole):
        self.undoer.recordEvent(self.setData,(index,self.data(index,role),role))
        ix = index.row()
        if type(self.list[ix]) in self.supportedBuiltins:
            self.list[ix] = value
        else:
            self.list[ix].setRole(value,role)
        self.dataChanged.emit(index,index,[role])
        return True
    
    def moveRow(self,sourceParent,sourceRow,destinationParent,destinationRow):
        return self.moveRows(sourceParent,sourceRow,1,destinationParent,destinationRow)
    
    def moveRows(self,sourceParent,sourceRow,count,destinationParent,destinationRow):
        if sourceParent.isValid():
            return False
        if destinationParent.isValid():
            return False
        self.beginMoveRows(sourceParent,sourceRow,sourceRow+count-1,destinationParent,destinationRow)
        six,dix,k = sourceRow,destinationRow,count
        self.undoer.recordEvent(self.moveRows,(destinationParent,dix,k,sourceParent,six))
        self.list[six:six+k],self.list[dix,dix] = self.list[dix,dix],self.list[six:six+k]
        self.endMoveRows()
        return True
    
    def insertRow(self,row,parent):
       return  self.insertRows(row,1,parent)
    
    def insertRows(self,row,count,parent):
        if parent.isValid():
            return False
        self.beginInsertRows(parent,row,row+count-1)
        self.undoer.recordEvent(self.removeRows,(row,count,parent))
        for r in range(row,row+count):
            self.list[r:r] = [NoneObject()]
        self.endInsertRows()
        return True
    
    def removeRow(self,row,parent):
        return self.removeRows(row,1,parent)
        
    def removeRows(self,row,count,parent):
        if parent.isValid():
            return False
        self.beginRemoveRows(parent,row,row+count-1)
        self.undoer.recordEvent(self.insertData,(self.list[row:row+count],row))
        self.list[row:row+count] = []        
        self.endRemoveRows()
        return True    
        
    def data(self,index,role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        ix = index.row()
        if type(self.list[ix]) in self.supportedBuiltins:
            if role == Qt.DisplayRole or role == Qt.EditRole:
                return self.list[ix]
        else:
            return self.list[ix].getRole(role)
    
    def rowCount(self,index):
        if index.isValid():
            return 0
        return len(self)
    
    def __eq__(self,otherObj):
        return all((l == r for l,r in zip(self,otherObj)))
    
    def __repr__(self):
        return repr(self.list)
    
    def __str__(self):
        return str(self.list)
    
    def __len__(self):
        return len(self.list)
    
    def __iter__(self):
        return iter(self.list)
    
    def __getitem__(self,key):
        if type(key) is int:
            if key < 0: key = len(self) + key
            return self.list[key]
            #self.data(self.index(key,0,QModelIndex()),Qt.DisplayRole)
        if type(key) is slice:
            start,end,step = self.sanitizeSlice(key)
            return QList([self.data[i] for i in range(start,end,step)])
        if iterable(key):
            return QList((self.data[key] for i in key))
        return self.data(key)
    
    def sanitizeSlice(self,key):
        start = 0 if key.start is None else key.start
        end = len(self) if key.stop is None else key.stop
        step = 1 if key.step is None else key.step
        return start,end,step
        
    def sliceSet(self,key,value):
        start,end,step = self.sanitizeSlice(key)
        if key.step is not None:
            indices = range(start,end,step)
            if any((not(0<=i<len(self))for i in indices)):
                self.undoer.discardRecording()
                self.undoer.stopRecording()
                raise ValueError("Invalid indices on extended slice")
            if not iterable(value) or len(indices) > len(value):
                self.undoer.stopRecording()
                self.undoer.discardRecording()
                raise ValueError("Attempt to assign sequence of invalid size to extended slice of size %d"%len(indices))
            for ix,val in zip(indices,value):
                self[ix] = val
            return
        
        if not iterable(value):
            value = [value]
            if not hasattr(value,"len"):
                value = list(value)
        if start == end:
            self.insertData(value,min(start,len(self)))
            return
        if start >= len(self):
            self.insertData(value)
            return
        if end < len(self):
            if end-start != len(value):
                excess = (end-start) - len(value)
                if excess > 0:
                    self.removeRows(start,excess,QModelIndex())
                else:
                    self.insertRows(end,excess,QModelIndex())
            for i,val in zip(range(start,end),value):
                self[i] = val
        if end > len(self):
            if start + len(value) <= len(self):
                self.removeRows(start+len(self),len(self)-(start+len(self)),QModelIndex())
                return
            else:
                self.insertRows(len(self),len(self)-(start+len(self)),QModelIndex())
            for i,v in zip(range(start,start+len(value)),value):
                self[i] = v
            return
    
    def __setitem__(self,key,value):
        self.undoer.startRecording()
        if type(key) is int:
            self.assign(key,value)
            #self.setData(self.index(key,0,QModelIndex()),value,Qt.EditRole)
        elif type(key) is slice:
            self.sliceSet(key,value)
        elif iterable(key):
            keys = reversed(sorted(iterable),key = lambda x: x%len(self))
            if iterable(value):
                for key,val in zip(keys,value):
                    self[key]=val
            else:
                for key in keys:
                    self[key]=value
        else:
            self.assign(key.row(),value)
            #self.setData(key,value,Qt.EditRole)
        self.undoer.stopRecording()
    
    def insertData(self,data,startIndex=None,assignContainer=False):
        if startIndex is None:
            startIndex = len(self)
        self.undoer.startRecording()
        if assignContainer or not iterable(data):
            self.insertRows(startIndex,1,QModelIndex())
            self.assign(self.index(len(self)-1,0,QModelIndex()),data)
        else:
            self.insertRows(startIndex,len(data),QModelIndex())
            for i,v in zip(range(startIndex,startIndex+len(data)),data):
                self.assign(self.index(i,0,QModelIndex()),v)
        self.undoer.stopRecording()
    def insert(self,index,value):
        self.insertData(value,index,assignContainer=True)
    def remove(self,index):
        self.removeRow(index,QModelIndex())
    def find(self,value,start=0,end=None):
        return self.list.index(value,start,end if end else len(self))
    def count(self,value):
        return self.count(value)
    def pop(self,index=None):
        if index == None:
            index = len(self)-1
        item = self[index]
        self.remove(index)
        return item
    def reverse(self):
        startindex = self.index(0,0,QModelIndex())
        endindex = self.index(len(self)-1,0,QModelIndex())
        self.undoer.recordEvent(self.reverse,())
        self.list.reverse()
        self.dataChanged.emit(startindex,endindex)
    def __add__(self,listCompatible):
        return QList(self.list+listCompatible)
    def __radd__(self,listCompatible):
        return QList(listCompatible + self.list)
    def extend(self,iterator):
        self.insertData(iterator)
    def clear(self):
        self.removeRows(0,len(self),QModelIndex)
    def append(self,value):
        self.insertData(value,assignContainer=True)
    def undo(self):
        self.undoer.undo()
    def redo(self):
        self.undoer.redo()
    def clearRedo(self):
        self.undoer.clearRedoQueue()
    def reset(self):
        while(self.undoer.undo()):
            pass

if __name__ in "__main__":
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    args = app.arguments()[1:]
    
    a = QList([12,3,4])
    from PyQt5.QtWidgets import QListView
    view = QListView()
    view.setModel(a)
    view.show()
    
    sys.exit(app.exec_())