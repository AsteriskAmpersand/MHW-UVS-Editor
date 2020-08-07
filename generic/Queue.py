# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 05:59:31 2020

@author: AsteriskAmpersand
"""


from collections import deque,Counter

class Queue(deque):
    def put(self,item):
        self.append(item)
    def get(self):
        return self.popleft()
    def peek(self):
        return self[0]
    def empty(self):
        return len(self)==0
    def consume(self):
        return iter(self)
        
    
class Stack(deque):
    def put(self,item):
        self.append(item)
    def get(self):
        return self.pop()
    def peek(self):
        return self[-1]
    def empty(self):
        return len(self)==0
    def consume(self):
        return iter(reversed(self))
    
class CopyStack(Stack):
    def __init__(self,*args,**kwargs):
        self.__pure__ = True
        self.__types__ = Counter()
        super().__init__(*args,**kwargs)
    def types(self):
        return ((key for key in self.__types__))
    def pure(self):
        return self.__pure__
    def put(self,item):
        if self.__types__:
            if type(item) not in self.__types__:
                self.__pure__ = False
        self.__types__.update([type(item)])
        super().put(item)
    def get(self):
        item = super().get()
        self.__types__.substract([type(item)])
        if self.__types__[item]<=0:
            del self.__types__[item]
            self.__pure__ = len(self.__types__)>1
        return item
    def clear(self):
        self.__pure__ = True
        self.__types__ = Counter()
        super().clear()
    def split(self):
        types = {t:CopyStack() for t in self.__types__}
        for entry in self.consume():
            types[type(entry)].put(entry)
        return types