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
        