# -*- coding: utf-8 -*-
"""
Created on Sat May  2 02:39:31 2020

@author: AsteriskAmpersand
"""


from PyQt5 import QtCore, QtGui, QtWidgets

class RichTextDisplay(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        options = QtWidgets.QStyleOptionViewItem (option)
        self.initStyleOption(options,index)

        style = QtGui.QApplication.style() if options.widget is None else options.widget.style()

        doc = QtGui.QTextDocument()
        doc.setHtml(options.text)

        options.text = ""
        style.drawControl(QtWidgets.QStyle.CE_ItemViewItem, options, painter);

        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()

        # Highlighting text if item is selected
        #if (optionV4.state & QStyle::State_Selected)
            #ctx.palette.setColor(QPalette::Text, optionV4.palette.color(QPalette::Active, QPalette::HighlightedText));

        textRect = style.subElementRect(QtWidgets.QStyle.SE_ItemViewItemText, options)
        painter.save()
        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter, ctx)

        painter.restore()

    def sizeHint(self, option, index):
        options = QtWidgets.QStyleOptionViewItem (option)
        self.initStyleOption(options,index)

        doc = QtGui.QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        return QtCore.QSize(doc.idealWidth(), doc.size().height())
    
"""
After line: doc.setHtml(options.text), you need to set also doc.setTextWidth(option.rect.width()), 
otherwise the delegate wont render longer content correctly in respect to target drawing area. 
For example does not wrap words in QListView. 
"""