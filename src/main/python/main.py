#!/usr/bin/env python

#region licensing

#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################

#ScribbleArea is a minimally modified version of the Scribble example that draws rectangles and adds undo functionality. The notice above is kept as a result.

#endregion licensing

#region imports
import PyQt5
from PyQt5.QtCore import QDir, QPoint, QRect, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QImageWriter, QPainter, QPen, qRgb, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QColorDialog, QFileDialog,
        QInputDialog, QMainWindow, QMenu, QMessageBox, QWidget, QTableWidgetItem)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
import webbrowser
#------
from rectmap import Ui_MainWindow
#------
appctxt = ApplicationContext()
imgpath = appctxt.get_resource('rovercourse.png')#gets relative/absolute path through fbs
#endregion imports

class ScribbleArea(QWidget):
    #this is a custom signal
    #it must be a class variable; it won't work if placed in __init__
    dataChanged = pyqtSignal()
    posChanged = pyqtSignal(int,int)
    def __init__(self, parent=None):
        
        super(ScribbleArea, self).__init__(parent)
        #super().__init__()

        #self.setAttribute(Qt.WA_StaticContents)
        self.modified = False
        self.scribbling = False
        self.myPenWidth = 1
        self.myPenColor = Qt.blue
        self.image = QImage()
        self.startingPoint = QPoint()
        self.endPoint = QPoint()
        self.rects = []

        self.setMouseTracking(True)
        #self.dataChanged = pyqtSignal()

    def openImage(self, fileName):
        loadedImage = QImage()
        if not loadedImage.load(fileName):
            return False

        newSize = loadedImage.size().expandedTo(self.size())
        self.resizeImage(loadedImage, newSize)
        self.image = loadedImage
        self.modified = False
        self.update()
        return True

    def saveImage(self, fileName, fileFormat):
        visibleImage = self.image
        self.resizeImage(visibleImage, self.size())

        if visibleImage.save(fileName, fileFormat):
            self.modified = False
            return True
        else:
            return False

    def setPenColor(self, newColor):
        self.myPenColor = newColor

    def setPenWidth(self, newWidth):
        self.myPenWidth = newWidth

    def clearImage(self):
        self.image.fill(qRgb(255, 255, 255))
        self.modified = True
        self.update()

    def undoLast(self):
        try:
            self.clearImage()
            del self.rects[-1]
            self.drawallRects()
            #we also need to update the table here
        except Exception as e:
            print(e)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startingPoint = event.pos()
            self.scribbling = True

    def mouseMoveEvent(self, event):
        self.posChanged.emit(event.pos().x(),event.pos().y())
        if (event.buttons() & Qt.LeftButton) and self.scribbling:
            self.rects.append(QRect(self.startingPoint,event.pos()))
            self.drawallRects()
            del self.rects[-1]
            #we can update the table here if it's not too resource consuming
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.scribbling:
            self.endPoint = event.pos()
            self.scribbling = False
            self.rects.append(QRect(self.startingPoint, self.endPoint))
            #here we should also add this data to the table and update it
            self.dataChanged.emit() #this says that the rectangle data has changed
            self.drawallRects()

    def paintEvent(self, event):
        painter = QPainter(self)
        dirtyRect = event.rect()
        painter.drawImage(dirtyRect, self.image, dirtyRect)

    def resizeEvent(self, event):
        if self.width() > self.image.width() or self.height() > self.image.height():
            newWidth = max(self.width() + 128, self.image.width())
            newHeight = max(self.height() + 128, self.image.height())
            self.resizeImage(self.image, QSize(newWidth, newHeight))
            self.update()

        super(ScribbleArea, self).resizeEvent(event)

    def drawallRects(self):
        '''
        is very inefficient because we don't just update the thing - no, we redraw *everything*
        a better way of doing this (i believe) is to use QGraphicsView since we don't need to store (and redraw) elements - it's done for us

        that said, i wasn't able to implement a proper rectangle deletion function properly without using this "array -> draw everything method" w/ QPainter
        it's also a good deal easier to mesh with the table widget and export it into a format i understand

        so maybe one day i'll refactor this but for now this is good enough without absolutely shredding through resources
        '''
        try:
            self.clearImage()
            painter = QPainter(self.image)
            painter.setPen(QPen(self.myPenColor, self.myPenWidth, Qt.SolidLine,
                    Qt.RoundCap, Qt.RoundJoin))
            #at this point we can redraw the image
            #painter.drawPixmap(QRect(0,0,50,50),QPixmap("rovercourse.png"))
            #painter.drawPixmap(QRect(0,0,self.frameGeometry().width(),self.frameGeometry().height()),QPixmap(imgpath))
            for rect in self.rects:
                painter.drawRect(rect)
            self.modified = True
            self.update()
        except Exception as e:
            print(e)

    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return

        newImage = QImage(newSize, QImage.Format_RGB32)
        newImage.fill(qRgb(255, 255, 255))
        painter = QPainter(newImage)
        painter.drawImage(QPoint(0, 0), image)
        self.image = newImage

    def print_(self):
        printer = QPrinter(QPrinter.HighResolution)

        printDialog = QPrintDialog(printer, self)
        if printDialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter(printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.image.rect())
            painter.drawImage(0, 0, self.image)
            painter.end()

    def isModified(self):
        return self.modified

    def penColor(self):
        return self.myPenColor

    def penWidth(self):
        return self.myPenWidth

class ApplicationWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("RectangleMappingTool")

        #self.scribbleArea = ScribbleArea()
        self.drawing_area = ScribbleArea(self.drawing_area)
        self.drawing_area.resize(400,300)
        self.drawing_area.dataChanged.connect(self.getData)
        self.drawing_area.posChanged.connect(self.updateCoords)

        self.pushButton.clicked.connect(self.adddata)
        self.pushButton_2.clicked.connect(self.removedata)

        self.actionUndo.triggered.connect(self.undo)
        self.actionPen_Color.triggered.connect(self.changePenColor)
        self.actionPen_Width.triggered.connect(self.changePenWidth)
        self.actionGitHub_Repository.triggered.connect(self.openGithub)
        self.actionAbout.triggered.connect(self.about)

        #self.resize(500, 500)
    def adddata(self,coords):
        row_number = self.table_widget.rowCount()+1
        self.table_widget.setRowCount(row_number) 
        self.table_widget.setItem(row_number-1,0,QTableWidgetItem(str(coords[0])))
        self.table_widget.setItem(row_number-1,1,QTableWidgetItem(str(coords[1])))
        self.table_widget.setItem(row_number-1,2,QTableWidgetItem(str(coords[2])))
        self.table_widget.setItem(row_number-1,3,QTableWidgetItem(str(coords[3]))) #row, column, QTableWidgetItem; zero-indexed

        #we can perform brute-force checking with QRect.intersects(<QRect2>)
        #should we? dunno
        #but if so, perhaps consider an "intersects with" column
    def removedata(self):
        self.table_widget.removeRow(3)
        del self.drawing_area.rects[2]
        self.drawing_area.drawallRects()
    def getData(self):
        #print(self.drawing_area.rects) #this gets our QRect objects, and we can just start getting data from here
        newrect = self.drawing_area.rects[len(self.drawing_area.rects)-1]
        self.adddata(newrect.getCoords())
    def updateCoords(self,x,y):
        self.coord_label.setText("x:"+str(x)+" y:"+str(y))
    #region Actions
    def undo(self):
        self.drawing_area.undoLast()
        #update table entries on undo
    def changePenColor(self):
        newColor = QColorDialog.getColor(self.drawing_area.penColor())
        if newColor.isValid():
            self.drawing_area.setPenColor(newColor)
    def changePenWidth(self):
        newWidth, ok = QInputDialog.getInt(self, "Set New Pen Width",
                "Select pen width:", self.drawing_area.penWidth(), 1, 50, 1)
        if ok:
            self.drawing_area.setPenWidth(newWidth)
    def about(self):
        QMessageBox.about(self, "About RectangleMappingTool",
                '<p>RectangleMappingTool is a program designed for the <a href="https://github.com/aacttelemetry">AACT Telemetry project</a>, built with PyQt5 and packaged through fbs.</p>'
                '<p>Its primary purpose is to make creating rectangular bounding regions based on an image easier.</p>'
                '<p>You can view the source and of this program and additional information <a href="https://github.com/aacttelemetry/RectangleMappingTool">here</a>.</p>')
    def openGithub(self):
        webbrowser.open("https://github.com/aacttelemetry/RectangleMappingTool")
    #endregion
'''
    def closeEvent(self, event):
        if self.savePrompt():
            event.accept()
        else:
            event.ignore()

    def open(self):
        if self.savePrompt():
            fileName, _ = QFileDialog.getOpenFileName(self, "Open File",
                    QDir.currentPath())
            if fileName:
                self.scribbleArea.openImage(fileName)

    def save(self):
        action = self.sender()
        fileFormat = action.data()
        self.saveFile(fileFormat)

    def savePrompt(self):
        #just close w/out prompting user
        #comment below
        if self.scribbleArea.isModified():
            ret = QMessageBox.warning(self, "Scribble",
                        "The image has been modified.\n"
                        "Do you want to save your changes?",
                        QMessageBox.Save | QMessageBox.Discard |
                        QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return self.saveFile('png')
            elif ret == QMessageBox.Cancel:
                return False
        #comment above
        return True

    def saveFile(self, fileFormat):
        initialPath = QDir.currentPath() + '/untitled.' + fileFormat

        fileName, _ = QFileDialog.getSaveFileName(self, "Save As", initialPath,
                "%s Files (*.%s);;All Files (*)" % (fileFormat.upper(), fileFormat))
        if fileName:
            return self.scribbleArea.saveImage(fileName, fileFormat)

        return False
    '''

class AppContext(ApplicationContext):          
    def run(self):                              
        aw = ApplicationWindow()
        aw.show()
        return self.app.exec_()                 

if __name__ == '__main__':
    appctxt = AppContext()                    
    exit_code = appctxt.run()          
    sys.exit(exit_code)