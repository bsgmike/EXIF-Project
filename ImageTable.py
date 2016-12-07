import sip
# switch on QString in Python3
sip.setapi('QString', 1)


from PyQt4 import QtGui, QtCore, uic


class ImageTableModel(QtCore.QAbstractTableModel):
    def __init__(self, images=[[]], headers=[], parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__images = images
        self.__headers = headers

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__images)

    def columnCount(self, parent):
        return len(self.__images[0])

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

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


        # if role == QtCore.Qt.DecorationRole:
        #     row = index.row()
        #     column = index.column()
        #     value = QtGui.QColor(0, 255, 0)
        #
        #     pixmap = QtGui.QPixmap(10, 10)
        #     pixmap.fill(value)
        #
        #     icon = QtGui.QIcon(pixmap)
        #     #eventually we want to return a jpg thumbnail here
        #     return icon

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__images[row][column]

            return value

    #Don't think we need this as the table won't be editable
    # def setData(self, index, value, role=QtCore.Qt.EditRole):
    #     if role == QtCore.Qt.EditRole:
    #
    #         row = index.row()
    #         column = index.column()
    #
    #         color = QtGui.QColor(value)
    #
    #         if color.isValid():
    #             self.__colors[row][column] = color
    #             self.dataChanged.emit(index, index)
    #             return True
    #     return False

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

        newValue = [fileName, dateTime, "New Name"]
        self.__images.insert(0, newValue)

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
