#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sip
# switch on QString in Python3
sip.setapi('QString', 1)

import sys
import os
import time

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, QDir
from PyQt4.QtGui import *
import exifread
import ImageTable
from os import listdir
from os.path import isfile, join
from datetime import datetime
from PIL import Image
from PIL.ImageQt import ImageQt


#from PyQt4 import QtCore, QtGui




#http://stackoverflow.com/questions/24106903/resizing-qpixmap-while-maintaining-aspect-ratio
class ImageLabel(QtGui.QLabel):
    def __init__(self, img):
        #QLabel.__init__()
        super(ImageLabel, self).__init__()
        self.setFrameStyle(QFrame.StyledPanel)
        # self.pixmap = QPixmap(img)

        self.size = 64, 64
        self.im = Image.open(img)
        self.im.thumbnail(self.size)



    def paintEvent(self, event):
        # size = self.size()
        painter = QtGui.QPainter(self)
        point = QtCore.QPoint(0,0)
        # scaledPix = self.pixmap.scaled(size, Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
        # start painting the label from left upper corner
        # point.setX((size.width() - scaledPix.width())/2)
        # point.setY((size.height() - scaledPix.height())/2)
        #print point.x(), ' ', point.y()
        myQtImage = ImageQt(self.im)
        pixmap = QtGui.QPixmap.fromImage(myQtImage)
        label = QtGui.QLabel('', self)
        label.setPixmap(pixmap)
        painter.drawPixmap(point,pixmap)

    def ChangePixmap(self, img):
        # self.pixmap = QtGui.QPixmap(img)
        self.im = Image.open(str(img))
        self.im.thumbnail(self.size)
        self.repaint()  # repaint() will trigger the paintEvent(self, event), this way the new pixmap will be drawn on the label

class MyButton(QPushButton):
    def __init__(self, text):
        super(MyButton, self).__init__()
        self.setFixedWidth(100)
        self.setFixedHeight(30)
        self.setFont(QtGui.QFont('SansSerif', 12))
        self.setStyleSheet("background-color: #FFF096; color: blue")
        # self.setStyleSheet("color: blue")
        self.setText(text)
    def close(self):
        self

    def deleteImageTable(self):
        global myBrowser
        myBrowser.clearTable()

    def InsertARow(self):
        global myBrowser
        myBrowser.model.insertRow(0, "testing ")


class Browser( QWidget):
    def __init__(self):
        super(Browser, self).__init__()

        self.resize(1400, 800)
        self.setWindowTitle("File Browser")
        self.treeView = QTreeView()
        self.fileSystemModel = QFileSystemModel(self.treeView)
        self.fileSystemModel.setReadOnly(False)
        self.fileSystemModel.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.Files)
        root = self.fileSystemModel.setRootPath("C:\\Users\\mbowley\\Pictures")
        self.treeView.setModel(self.fileSystemModel)
        self.treeView.setRootIndex(root)
        self.treeView.setColumnWidth(0, 200)
        self.treeView.clicked.connect(self.on_treeView_clicked)


        # self.label = QLabel()
        # self.pixmap = QPixmap(os.getcwd() + '/eclipse.png')
        # self.label.setPixmap(self.pixmap)

        self.label2 = ImageLabel("python.png")

        #Create some buttons
        self.closeButton = MyButton("Exit")
        self.runButton = MyButton("Run")
        self.dirButton = MyButton("Set Dir")
        self.clearButton = MyButton("Clear")
        self.insertButton = MyButton("Insert")


        # Create textboxes
        self.fileNametextbox = QLineEdit()
        self.fileNametextbox.move(200, 20)
        self.fileNametextbox.resize(20, 180)

        self.pathNametextbox = QLineEdit()
        self.pathNametextbox.move(200, 20)
        self.pathNametextbox.resize(20, 180)

        # create QLabels
        self.filepathLabel = QLabel()
        self.filepathLabel.setText("python.jpg")
        self.filepathLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken);
        self.filepathLabel.setFixedWidth(200)
        self.filepathLabel.setFixedHeight(40)
        self.filepathLabel.setFont(QtGui.QFont('SansSerif', 14))

        self.exifLabel = QLabel()
        self.exifLabel.setText("Exif data goes here")
        self.exifLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken);
        self.exifLabel.setFixedWidth(400)
        self.exifLabel.setFixedHeight(240)
        self.exifLabel.setFont(QtGui.QFont('SansSerif', 8))

        # create textbox for tags
        self.tagtextBox = QTextEdit()
        self.tagtextBox.setText("Exif data goes here")
        self.tagtextBox.setFixedWidth(500)
        self.tagtextBox.setFixedHeight(240)
        self.tagtextBox.setFont(QtGui.QFont('SansSerif', 8))


        LeftPanelLayout = QHBoxLayout()
        RightPanelLayout = QVBoxLayout()
        TopLevelPanelLayout = QHBoxLayout()
        TopLevelLayout = QVBoxLayout()
        ButtonBar = QHBoxLayout()

        #put the file browser into the left panel
        LeftPanelLayout.addWidget(self.treeView)

        #add the textbox and picture into the right hand panel
        RightPanelLayout.addWidget(self.fileNametextbox)
        RightPanelLayout.addWidget(self.pathNametextbox)
        RightPanelLayout.addWidget(self.filepathLabel)
        # RightPanelLayout.addWidget(self.exifLabel)
        RightPanelLayout.addWidget(self.tagtextBox)
        RightPanelLayout.addWidget(self.label2)

        # add the buttons to the button bar
        ButtonBar.addWidget(self.closeButton)
        ButtonBar.addWidget(self.runButton)
        ButtonBar.addWidget(self.dirButton)
        ButtonBar.addWidget(self.clearButton)
        ButtonBar.addWidget(self.insertButton)
        ButtonBar.setAlignment(Qt.AlignLeft)

        self.tableView = QtGui.QTableView()
        self.tableView.setSortingEnabled(True)
        self.tableView.verticalHeader().setDefaultSectionSize(64);
        self.tableView.show()

        headers = ["Old Image Name", "Date Taken", "DateTime", "New Image name"]
        rowCount = 4
        default_datetime = datetime.strptime('1964:05:03 12:34:56', '%Y:%m:%d %H:%M:%S')
        tableData0 = [["testing.jpg", "03/05/1964", default_datetime, "image 1 1964"]for j in range(rowCount)]
        self.model = ImageTable.ImageTableModel(tableData0, headers)
        self.tableView.setModel(self.model)
        self.tableView.setColumnHidden(2, True)

        #Add the left and right layouts into the top level layout
        TopLevelPanelLayout.addLayout(LeftPanelLayout)
        TopLevelPanelLayout.addLayout(RightPanelLayout)
        TopLevelPanelLayout.addWidget(self.tableView)

        # add the panel layout and the button bar into the top level layout
        TopLevelLayout.addLayout(TopLevelPanelLayout)
        TopLevelLayout.addLayout(ButtonBar)
        self.setLayout(TopLevelLayout)

        self.closeButton.clicked.connect(self.close)
        self.clearButton.clicked.connect(MyButton.deleteImageTable)
        self.insertButton.clicked.connect(self.close)

    def clearTable(self):
        self.model.removeAllRows()

    def insertOneRow(self):
        label = time.strftime('%X %x %Z')
        label = "test" + label
        self.model.insertRow(0, label)


    def on_treeView_clicked(self, index):
        item = self.treeView.selectedIndexes()[0]
        indexItem = self.fileSystemModel.index(index.row(), 0, index.parent())

        fileName = self.fileSystemModel.fileName(indexItem)
        filePath = self.fileSystemModel.filePath(indexItem)
        self.model.setBaseDir(filePath)

        # f = open(str(filePath), 'rb')
        # tags = exifread.process_file(f, stop_tag='DateTimeOriginal')
        # f.close()

        if os.path.isdir(str(filePath)):
            onlyfiles = [f for f in listdir(str(filePath)) if isfile(join(str(filePath), f))]
            if self.model.removeAllRows() == True:
                self.tableView.clearSpans()
                for file in onlyfiles:
                    f = open(join(str(filePath), file), 'rb')
                    tags = exifread.process_file(f, stop_tag='DateTimeOriginal', strict=True)
                    f.close()
                    if 'EXIF DateTimeOriginal' in tags:
                    # self.model.insertRow(0, str(file)+time.strftime('%X %x %Z'))
                        self.model.insertRow(0, str(file), str(tags['EXIF DateTimeOriginal']))
                    else:
                        self.model.insertRow(0, str(file), "No date tag")
            else:
                print("Whoops")


        self.fileNametextbox.setText(fileName)
        self.pathNametextbox.setText(filePath)
        self.pixmap = QPixmap(filePath)

        self.filepathLabel.setText(fileName)
        #self.label.setPixmap(self.pixmap)
        #self.label.resize(640,480)

        self.label2.ChangePixmap(filePath)


        self.exifLabel.setText("")
        tagStr = ""
        f = open(str(filePath), 'rb')
        tags = exifread.process_file(f, stop_tag='DateTimeOriginal', strict=True)
        f.close()
        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                # print
                # "Key: %s, value %s" % (tag, tags[tag])
                tagStr = tagStr + "Key: %s, value %s" % (tag, tags[tag])
                tagStr = tagStr + "\r"
                self.tagtextBox.setText(tagStr)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myBrowser = Browser()

    myBrowser.show()
sys.exit(app.exec_())
