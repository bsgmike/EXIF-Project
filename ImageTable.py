import sip
# switch on QString in Python3
sip.setapi('QString', 1)


import operator
from os.path import isfile, join
from PyQt4 import QtGui, QtCore, uic
from datetime import datetime

from PyQt4.QtCore import *
from PIL import Image
from PIL.ImageQt import ImageQt

class ImageTableModel(QtCore.QAbstractTableModel):
    def __init__(self, datain, thumbRes, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        # self.__images = images
        # self.__headers = headers
        self.order = QtCore.Qt.DescendingOrder
        self.baseDir = "C:\\"
        self.size = 64, 64
        self.im = Image.open("python.png")
        self.im.thumbnail(self.size)
        self.pixmap_cache = {}
        self._thumbRes = thumbRes
        self._listdata = datain

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__images)

    def columnCount(self, parent):
        return len(self.__images[0])

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setBaseDir(self, baseDir):
        self.baseDir = baseDir

    def data(self, index, role):

        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            return self.__images[row][column].name()

        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            column = index.column()
            if column == 0:
                return "Image name: " + self.__images[row][column].name()
            if column == 1:
                return "Date taken: " + self.__images[row][column].name()
            if column == 2:
                return "New File Name: " + self.__images[row][column].name()

        if role == QtCore.Qt.DecorationRole:
            # row = index.row()
            # column = index.column()
            # value = QtGui.QColor(0, 255, 0)

            pixmap = QtGui.QPixmap(64, 64)
            # pixmap.fill(value)
            # pixmap.load("python.png")
            # icon = QtGui.QIcon(pixmap)

            # if column == 0:
            #     img = join(str(self.baseDir), str(self.__images[row][column]))
            #     print(img)
            #     if isfile(img):
            #         self.im = Image.open(img)
            #         self.im.thumbnail(self.size)
            #         myQtImage = ImageQt(self.im)
            #         pixmap = QtGui.QPixmap.fromImage(myQtImage)
            #     else:
            #         self.im = Image.open("python.png")
            #         self.im.thumbnail(self.size)
            #         myQtImage = ImageQt(self.im)
            #         pixmap = QtGui.QPixmap.fromImage(myQtImage)
            #
            #     icon = QtGui.QIcon(pixmap)
            #     # return icon
            #     return pixmap
            # else:
            #     return False

            row = index.row()
            column = index.column()
            if column == 0:
                try:
                    value = self._listdata[row]
                except IndexError:
                    return

                pixmap = None
                # value is image path as key

                pixmap = self.pixmap_cache.get(value)
                if pixmap == None:
                    pixmap = self.generatePixmap(value)
                    self.pixmap_cache[value] = pixmap

                # if value in self.pixmap_cache is False:
                #     pixmap=self.generatePixmap(value)
                #     self.pixmap_cache[value] =  pixmap
                # else:
                #     pixmap = self.pixmap_cache[value]
                return QtGui.QImage(pixmap).scaled(self._thumbRes[0], self._thumbRes[1],
                                                   QtCore.Qt.KeepAspectRatio)
            else:
                return False

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__images[row][column]

            return value

    def generatePixmap(self, value):
        pixmap=QtGui.QPixmap()
        pixmap.load(value)
        return pixmap

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:

                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return "not implemented"
            else:
                return QtCore.QString("Image  %1  ").arg(section)

    # =====================================================#
    # INSERTING & REMOVING
    # =====================================================#
    def insertRows(self, position, rows, fileName, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)

        for i in range(rows):
            defaultValues = [fileName, "Date Taken", "New Name"]
            self.__images.insert(position, defaultValues)

        self.endInsertRows()

        return True

    def insertRow(self, position=0, fileName="default.jpg", dateTime="1/1/1900", parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, 0, 0)
        datetime_object = datetime.strptime(dateTime, '%Y:%m:%d %H:%M:%S')
        newValue = [fileName, dateTime, datetime_object, "New Name"]
        # self.__images.insert(0, newValue)

        pixmap = self.pixmap_cache.get(value)
        if pixmap == None:
            pixmap = self.generatePixmap(value)
            self.pixmap_cache[value] = pixmap
        self.endInsertRows()
        return True

    def removeAllRows(self, parent=QtCore.QModelIndex()):
        count = self.rowCount() - 1
        self.beginRemoveRows(parent, 0, count)

        for i in range(count, 0, -1):
            value = self.__images[i]
            self.__images.remove(value)

        self.endRemoveRows()
        return True

    def toDateTime(self, dateTimeStr="2016:08:17 12:36:08"):
        datetime_object = datetime.strptime(dateTimeStr, '%Y:%m:%d %H:%M:%S')
        return datetime_object

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.__images = sorted(self.__images, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.__images.reverse()
        self.emit(SIGNAL("layoutChanged()"))

    #We won't be inserting columns
    # def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
    #     self.beginInsertColumns(parent, position, position + columns - 1)
    #
    #     rowCount = len(self.__colors)
    #
    #     for i in range(columns):
    #         for j in range(rowCount):
    #             self.__colors[j].insert(position, QtGui.QColor("#000000"))
    #
    #     self.endInsertColumns()
    #
    #     return True


#
# class ImageTableModel(QtCore.QAbstractTableModel):
#     def __init__(self, images=[[]] ,headers=[], parent=None):
#         QtCore.QAbstractTableModel.__init__(self, parent)
#         self.__images = images
#         self.__headers = headers
#         self.order = QtCore.Qt.DescendingOrder
#         self.baseDir = "C:\\"
#         self.size = 64, 64
#         self.im = Image.open("python.png")
#         self.im.thumbnail(self.size)
#
#     def rowCount(self, parent=QtCore.QModelIndex()):
#         return len(self.__images)
#
#     def columnCount(self, parent):
#         return len(self.__images[0])
#
#     def flags(self, index):
#         return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
#
#     def setBaseDir(self, baseDir):
#         self.baseDir = baseDir
#
#     def data(self, index, role):
#
#         if role == QtCore.Qt.EditRole:
#             row = index.row()
#             column = index.column()
#             return self.__images[row][column].name()
#
#         if role == QtCore.Qt.ToolTipRole:
#             row = index.row()
#             column = index.column()
#             if column == 0:
#                 return "Image name: " + self.__images[row][column].name()
#             if column == 1:
#                 return "Date taken: " + self.__images[row][column].name()
#             if column == 2:
#                 return "New File Name: " + self.__images[row][column].name()
#
#         if role == QtCore.Qt.DecorationRole:
#             row = index.row()
#             column = index.column()
#             value = QtGui.QColor(0, 255, 0)
#
#             pixmap = QtGui.QPixmap(64, 64)
#             # pixmap.fill(value)
#             # pixmap.load("python.png")
#             # icon = QtGui.QIcon(pixmap)
#
#             if column == 0:
#                 img = join(str(self.baseDir), str(self.__images[row][column]))
#                 print(img)
#                 if isfile(img):
#                     self.im = Image.open(img)
#                     self.im.thumbnail(self.size)
#                     myQtImage = ImageQt(self.im)
#                     pixmap = QtGui.QPixmap.fromImage(myQtImage)
#                 else:
#                     self.im = Image.open("python.png")
#                     self.im.thumbnail(self.size)
#                     myQtImage = ImageQt(self.im)
#                     pixmap = QtGui.QPixmap.fromImage(myQtImage)
#
#                 icon = QtGui.QIcon(pixmap)
#                 # return icon
#                 return pixmap
#             else:
#                 return False
#
#         if role == QtCore.Qt.DisplayRole:
#             row = index.row()
#             column = index.column()
#             value = self.__images[row][column]
#
#             return value
#
#     #Don't think we need this as the table won't be editable
#     # def setData(self, index, value, role=QtCore.Qt.EditRole):
#     #     if role == QtCore.Qt.EditRole:
#     #
#     #         row = index.row()
#     #         column = index.column()
#     #
#     #         color = QtGui.QColor(value)
#     #
#     #         if color.isValid():
#     #             self.__colors[row][column] = color
#     #             self.dataChanged.emit(index, index)
#     #             return True
#     #     return False
#
#     def headerData(self, section, orientation, role):
#
#         if role == QtCore.Qt.DisplayRole:
#
#             if orientation == QtCore.Qt.Horizontal:
#
#                 if section < len(self.__headers):
#                     return self.__headers[section]
#                 else:
#                     return "not implemented"
#             else:
#                 return QtCore.QString("Image  %1  ").arg(section)
#
#     # =====================================================#
#     # INSERTING & REMOVING
#     # =====================================================#
#     def insertRows(self, position, rows, fileName, parent=QtCore.QModelIndex()):
#         self.beginInsertRows(parent, position, position + rows - 1)
#
#         for i in range(rows):
#             defaultValues = [fileName, "Date Taken", "New Name"]
#             self.__images.insert(position, defaultValues)
#
#         self.endInsertRows()
#
#         return True
#
#     def insertRow(self, position=0, fileName="default.jpg", dateTime="1/1/1900", parent=QtCore.QModelIndex()):
#         self.beginInsertRows(parent, 0, 0)
#         datetime_object = datetime.strptime(dateTime, '%Y:%m:%d %H:%M:%S')
#         newValue = [fileName, dateTime, datetime_object, "New Name"]
#         self.__images.insert(0, newValue)
#
#         self.endInsertRows()
#
#         return True
#
#     def removeAllRows(self, parent=QtCore.QModelIndex()):
#         count = self.rowCount() - 1
#         self.beginRemoveRows(parent, 0, count)
#
#         for i in range(count, 0, -1):
#             value = self.__images[i]
#             self.__images.remove(value)
#
#         self.endRemoveRows()
#         return True
#
#     def toDateTime(self, dateTimeStr="2016:08:17 12:36:08"):
#         datetime_object = datetime.strptime(dateTimeStr, '%Y:%m:%d %H:%M:%S')
#         return datetime_object
#
#     def sort(self, Ncol, order):
#         #Sort table by given column number.
#
#         self.emit(SIGNAL("layoutAboutToBeChanged()"))
#         self.__images = sorted(self.__images, key=operator.itemgetter(Ncol))
#         if order == Qt.DescendingOrder:
#             self.__images.reverse()
#         self.emit(SIGNAL("layoutChanged()"))
#
#     #We won't be inserting columns
#     # def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
#     #     self.beginInsertColumns(parent, position, position + columns - 1)
#     #
#     #     rowCount = len(self.__colors)
#     #
#     #     for i in range(columns):
#     #         for j in range(rowCount):
#     #             self.__colors[j].insert(position, QtGui.QColor("#000000"))
#     #
#     #     self.endInsertColumns()
#     #
#     #     return True
