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

#region todo
'''process:
introduction
user loads an image (or doesn't)
user draws pretty rectangles
user defines top-left and lower-right equivalents (or doesn't, in which case the existing values are sent to the final step)
set drawing area and label to 0 size, add columns to table defining the new regions (gps coordinates, in our case)
allow user to define f-string
allow user to export table values as a .csv (and .txt for f-string)

---
implement functionality allowing user to import a .csv, stripping the values from that
'''
#endregion

#region imports
import PyQt5
from PyQt5.QtCore import QDir, QPoint, QRect, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QImageWriter, QPainter, QPen, qRgb, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QColorDialog, QFileDialog,
        QInputDialog, QMainWindow, QMenu, QMessageBox, QWidget, QTableWidgetItem, QGridLayout)
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

        #self.setAttribute(Qt.WA_StaticContents)
        self.modified = False
        self.scribbling = False
        self.myPenWidth = 1
        self.myPenColor = Qt.blue
        self.image = QImage()
        self.startingPoint = QPoint()
        self.endPoint = QPoint()
        self.rects = []

        #A QWidget normally only receives mouse move events (mouseMoveEvent) when a mouse button is being pressed. This sets it to always receive mouse events, regardless.
        self.setMouseTracking(True)
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
            self.dataChanged.emit() #this is used for "real-time" table updates
            del self.rects[-1]
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
            bg_img = QPixmap(imgpath)
            #print(bg_img.height())
           # print(bg_img.width())
            #bg_img_width = bg_img.width()
            #bg_img_height = bg_img.height()
            if bg_img.width() > self.frameGeometry().width():
                final_height = (bg_img.height()*self.frameGeometry().width())/bg_img.width()
               # print(final_height)
                final_width = self.frameGeometry().width()
                painter.drawPixmap(QRect(0,0,final_width,final_height),bg_img)
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
        '''
        See https://stackoverflow.com/questions/35185113/configure-qwidget-to-fill-parent-via-layouts.
        this appears to be the same issue in which this new widget is initialized to a 100px by 25px area
        so we create a new grid layout and place drawing_area into it
        this also affords us some flexibility if we ever want to hide drawing_area and place something different in container_left
        '''
        self.drawing_area = ScribbleArea(self.container_left)
        left_layout = QGridLayout()
        left_layout.addWidget(self.drawing_area, 0, 0, 1, 1)
        self.container_left.setLayout(left_layout)

        #self.drawing_area.resize(400,300)
        self.drawing_area.dataChanged.connect(self.updatetable)
        self.drawing_area.posChanged.connect(self.updateCoords)

        self.pushButton.clicked.connect(self.makebigger)
        self.pushButton_2.clicked.connect(self.removedata)

        self.actionUndo.triggered.connect(self.undo)
        self.actionPen_Color.triggered.connect(self.changePenColor)
        self.actionPen_Width.triggered.connect(self.changePenWidth)
        self.actionGitHub_Repository.triggered.connect(self.openGithub)
        self.actionAbout.triggered.connect(self.about)

        self.check_overlapping = True

        #this needs to be thrown into a function later
        if not self.check_overlapping:
            self.table_widget.setColumnCount(4) 

        #self.resize(500, 500)
    def makebigger(self):
        '''
        new_h = self.drawing_area.size().height() + 75
        print(self.drawing_area.size().height())
        print(new_h)
        new_w = self.drawing_area.size().width() + 100
        self.drawing_area.resize(new_w,new_h)
        '''
        print(self.table_widget.item(0,1).text())
    def updatetable(self):
        #i hate this
        #but i want to finish other functionality before turning to efficiency changes so here we are
        self.table_widget.setRowCount(0)

        for row_number in range(0,len(self.drawing_area.rects)):
            coords = self.drawing_area.rects[row_number].getCoords()
            #print("adding row %s" % str(int(row_number)+1))
            self.table_widget.setRowCount(row_number+1) 
            self.table_widget.setItem(row_number,0,QTableWidgetItem(str(coords[0])))
            self.table_widget.setItem(row_number,1,QTableWidgetItem(str(coords[1])))
            self.table_widget.setItem(row_number,2,QTableWidgetItem(str(coords[2])))
            self.table_widget.setItem(row_number,3,QTableWidgetItem(str(coords[3]))) #row, column, QTableWidgetItem; zero-indexed
            self.table_widget.setItem(row_number,4,QTableWidgetItem(""))

        #we can perform brute-force checking with QRect.intersects(<QRect2>)
        #the algorithm below checks each possible overlap, one-by-one (but does not check the same two rectangles for overlap twice)
        #add an "overlaps with" column if this is enabled
        if self.check_overlapping:
            rectangles = self.drawing_area.rects
            #we clear the entire column on each full overlap check
            #while implementing an array for each cell would be much better for various calculations and operations
            #maybe later
            for row_number in range(0,len(rectangles)):
                self.table_widget.setItem(row_number,4,QTableWidgetItem(""))
            for rect1_index in range(0,len(rectangles)):
                for rect2_index in range(rect1_index+1,len(rectangles)):
                    intersects = rectangles[rect1_index].intersects(rectangles[rect2_index])
                    #print(rectangles[rect1_index].intersects(rectangles[rect2_index]))
                    #print(f"Rectangle {rect1_index} overlaps with {rect2_index}?"+str(intersects))
                    current = self.table_widget.item(rect1_index,4).text()
                    current2 = self.table_widget.item(rect2_index,4).text()
                    if intersects:
                        if current == "":
                            self.table_widget.setItem(rect1_index,4,QTableWidgetItem(str(rect2_index+1)))
                        else:
                            self.table_widget.setItem(rect1_index,4,QTableWidgetItem(current+","+str(rect2_index+1)))
                        if current2 == "":
                            self.table_widget.setItem(rect2_index,4,QTableWidgetItem(str(rect1_index+1)))
                        else:
                            self.table_widget.setItem(rect2_index,4,QTableWidgetItem(current+","+str(rect1_index+1)))
            #print("---")
    def removeLast(self):
        self.table_widget.removeRow(self.table_widget.rowCount()-1)
    def removedata(self):
        self.table_widget.removeRow(3)
        del self.drawing_area.rects[2]
        self.drawing_area.drawallRects()
    def updateCoords(self,x,y):
        self.coord_label.setText("x:"+str(x)+" y:"+str(y))
    #region Actions
    def undo(self):
        self.drawing_area.undoLast()
        self.table_widget.removeRow(self.table_widget.rowCount()-1)#delete most recent table entry on undo
    def changePenColor(self):
        newColor = QColorDialog.getColor(self.drawing_area.penColor())
        print(newColor.getRgb()) #returns a standard tuple
        print(newColor.getRgb()[2])
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