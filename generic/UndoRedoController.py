# -*- coding: utf-8 -*-
"""
Created on Sat May  2 05:11:27 2020

@author: AsteriskAmpersand
"""
from generic.Queue import Queue,Stack

class ComplexAction():
    def __init__(self,parent,stack):
        self.actionStack = stack
        self.parent = parent
    def toEvent(self):
        raise NotImplementedError

class SelfInvertingAction(ComplexAction):
    def toEvent(self):
        return self.do,()
    def do(self):
        stack = self.actionStack
        self.parent.startRecording()
        for event in stack.consume():
            (doF,doP) = event
            doF(*doP)
        self.parent.stopRecording()
            
class ExplicitAction(ComplexAction):
    def toEvent(self):
        inverseStack = Stack()
        for event in self.actionStack.consume():
            (doF,doP),(undoF,undoP) = event
            inverseStack.put(((undoF,undoP),(doF,doP)))
        self.inverseStack = inverseStack
        return ((self.do(self.actionStack)),(self.do(self.inverseStack)))
    def do(self,stack):
        for event in stack.consume():
            (_,_),(doF,doP) = event
            doF(*doP)
            
class CountingStack(Stack):
    def addDepth(self):
        self.put(0)
    def count(self):
        self[-1]+=1
    def increase(self,val):
        self[-1]+=val

class UndoRedoController():
    def __init__(self):
        self.depth = 0
        self.depthStack = CountingStack()
        self.undoStack = Stack()
        self.redoStack = Stack()
        self.complexUndo = None
    def empty(self):
        return self.undoStack.empty()
    def recordEvent(self,event):
        if self.complexUndo is None:
            self.undoStack.put(event)
        else:
            self.depthStack.count()
            self.complexUndo.put(event)
    def startRecording(self):
        self.complexUndo = Stack()
        self.depthStack.addDepth()
        self.depth+=1        
    def stopRecording(self):
        if self.depth == 0:
            raise ValueError("No recording to End")
        self.depth -= 1        
        if self.depth == 0:
            ca = self.ActionClass(self,self.complexUndo)
            self.complexUndo = None   
            self.recordEvent(*ca.toEvent())
        val = self.depthStack.get()
        if not self.depthStack.empty():
            self.depthStack.increase(val)
        
    def discardCurrent(self):
        if self.complexUndo is None:
            raise ValueError("No Recording to Clear")
        count = self.depthStack.get()
        for i in range(count):
            self.complexUndo.get()
    def discardCompletely(self):
        if self.complexUndo is None:
            raise ValueError("No Recording to Clear")
        self.complexUndo.clear()
    def clearRedoStack(self):
        self.redoStack.clear()

class InvertingUndoRedoController(UndoRedoController):
    ActionClass = SelfInvertingAction
    def __init__(self):
        self.Forward = True
        super().__init__()
    def undo(self):
        if not self.undoStack.empty():
            self.Forward = False
            undoF,undoP = self.undoStack.get()
            undoF(*undoP)
            self.redoStack.put(self.undoStack.get())
            self.Forward = True
            return True
        else:
            return False
    def redo(self):
        if not self.redoStack.empty():
            doF,doP = self.redoStack.get()
            doF(*doP)
            return True
        else:
            return False
    def recordEvent(self,undoF,undoP):
        if self.Forward:
            self.clearRedoStack()
        super().recordEvent((undoF,undoP))
        
class ExplicitUndoRedoController(UndoRedoController):
    ActionClass = ExplicitAction
    def __init__(self):
        self.disabled = False
        super().__init__()
    def do(self,get,put,choice):
        doF,undoF = get()
        actionF,actionP = [doF,undoF][choice]
        self.disabled = True
        actionF(*actionP)
        self.disabled = False
        put((doF,undoF))
    def undo(self):
        if not self.undoStack.empty():
            self.do(self.undoStack.get,
                    self.redoStack.put,
                    1)
            return True
        return False
    def redo(self):
        if not self.redoStack.empty():
            self.do(self.redoStack.get,
                    self.undoStack.put,
                    0)   
            return True
        return False
    def recordEvent(self,doF,doP,undoF,undoP):
        if self.disabled:
            return
        self.clearRedoStack()
        super().recordEvent(((doF,doP),(undoF,undoP)))
    def startRecording(self):
        if self.disabled:
            return
        super().startRecording()
    def stopRecording(self):
        if self.disabled:
            return
        super().stopRecording()
    def discardCurrent(self):
        if self.disabled:
            return
    def discardCompletely(self):
        if self.disabled:
            return
        super().discardCompletely()
    def clearRedoStack(self):
        if self.disabled:
            return
        super().clearRedoStack(self)
        
class DummyRedoController(UndoRedoController):
    def __init__(self,*args,**kwargs):pass
    def empty(self,*args,**kwargs):pass
    def recordEvent(self,*args,**kwargs):pass
    def startRecording(self,*args,**kwargs):pass 
    def stopRecording(self,*args,**kwargs):pass        
    def discardCurrent(self,*args,**kwargs):pass
    def discardCompletely(self,*args,**kwargs):pass
    def clearRedoStack(self,*args,**kwargs):pass