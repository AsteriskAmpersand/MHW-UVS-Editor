# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 21:27:41 2020

@author: AsteriskAmpersand
"""

from PyQt5.QtWidgets import QListWidgetItem

class UVGroup(QListWidgetItem):
    def __init__(self,name,framedata,tpaths,ttypes,dynamic):
        super().__init__(name)
        self.framedata = framedata
        self.paths = tpaths
        self.types = ttypes
        self.dynamic = dynamic

    def indexize(self,pathdata):
        pathlist = [p for p,t in pathdata]
        self.indices = [pathlist.index(path) for path in self.paths]

    def clone(self):
        return UVGroup(self.text(), self.framedata,self.paths,self.types,self.dynamic)

    def virtual(self):
        return VirtualGroup(self.framedata,[p for p in self.paths],[t for t in self.types],self.dynamic)


class VirtualGroup():
    def __init__(self,framedata,tpaths,ttypes,dynamic):
        self.framedata = framedata
        self.paths = tpaths
        self.types = ttypes
        self.dynamic = dynamic

    def clone(self):
        return UVGroup(self.framedata,self.paths,self.types,self.dynamic)

    def indexize(self,pathdata):
        pathlist = [p for p,t in pathdata]
        self.indices = [pathlist.index(path) for path in self.paths]

    def split(self):
        newGroups = []
        for i in range(0,len(self.framedata),256):
            newGroups.append(VirtualGroup(self.framedata[i:min(i+256,len(self.framedata))],self.paths,self.types,self.dynamic))
        return newGroups