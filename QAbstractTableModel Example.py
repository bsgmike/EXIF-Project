import sys
import os

from PyQt4 import QtGui, QtCore

class MyListModel(QtCore.QAbstractTableModel):
    def __init__(self, datain, col, thumbRes, parent=None):
        """ datain: a list where each item is a row
        """
        self._thumbRes = thumbRes
        QtCore.QAbstractListModel.__init__(self, parent)
        self._listdata = datain
        self._col = col
        self.pixmap_cache = {}

    def colData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            return None

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation in [QtCore.Qt.Vertical, QtCore.Qt.Horizontal]:
                return None

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._listdata)

    def columnCount(self, parent):
        return self._col

    def data(self, index, role):
        if role == QtCore.Qt.SizeHintRole:
            return  QtCore.QSize(*self._thumbRes)

        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter

        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            try:
                fileName = os.path.split(self._listdata[row][column])[-1]
            except IndexError:
                return
            return fileName

        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            column = index.column()
            try:
                self.selectonChanged(row,column)
                fileName = os.path.split(self._listdata[row][column])[-1]
            except IndexError:
                return
            return QtCore.QString(fileName)

        if index.isValid() and role == QtCore.Qt.DecorationRole:
            row = index.row()
            column = index.column()
            try:
                value = self._listdata[row][column]
            except IndexError:
                return

            pixmap = None
            # value is image path as key
            # if self.pixmap_cache.has_key(value) == False:
            pixmap = self.pixmap_cache.get(value)
            if pixmap == None:
                pixmap = self.generatePixmap(value)
                self.pixmap_cache[value] = pixmap


            # if value in self.pixmap_cache is False:
            #     pixmap=self.generatePixmap(value)
            #     self.pixmap_cache[value] =  pixmap
            # else:
            #     pixmap = self.pixmap_cache[value]
            return QtGui.QImage(pixmap).scaled(self._thumbRes[0],self._thumbRes[1],
                QtCore.Qt.KeepAspectRatio)

        if index.isValid() and role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            try:
                value = self._listdata[row][column]
                fileName = os.path.split(value)[-1]
            except IndexError:
                return
            return os.path.splitext(fileName)[0]

    def generatePixmap(self, value):
        pixmap=QtGui.QPixmap()
        pixmap.load(value)
        return pixmap

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            try:
                newName = os.path.join(str(os.path.split(self._listdata[row][column])[0]), str(value.toString()))
            except IndexError:
                return
            self.__renameFile(self._listdata[row][column], newName)
            self._listdata[row][column] = newName
            self.dataChanged.emit(index, index)
            return True
        return False

    def selectonChanged(self, row, column):
        # TODO Image scale
        pass


    def __renameFile(self, fileToRename, newName):
        try:
            os.rename(str(fileToRename), newName)
        # except Exception, err:
        #     print(str(err))
        except Exception:
            print("Exception when renaming file")


class MyTableView(QtGui.QTableView):
    """docstring for MyTableView"""
    def __init__(self):
        super(MyTableView, self).__init__()
        self.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.FramelessWindowHint | QtCore.Qt.X11BypassWindowManagerHint)
        sw = QtGui.QDesktopWidget().screenGeometry(self).width()
        sh = QtGui.QDesktopWidget().screenGeometry(self).height()
        self.setGeometry(0,0,sw,sh)
        self.showFullScreen()

        thumbWidth = 320
        thumbheight = 240
        col = sw/thumbWidth
        self.setColumnWidth(thumbWidth, thumbheight)
        crntDir = "/Users/UserName/Pictures/"
        crntDir = r"C:\My Pictures\best\Beltring\2008"
        # create table
        list_data = []
        philes = os.listdir(crntDir)
        for phile in philes:
            if phile.endswith(".png") or phile.endswith(".jpg") or phile.endswith(".JPG"):
                list_data.append(os.path.join(crntDir, phile))
        # _twoDLst = convertToTwoDList(list_data, col)
        _twoDLst = convertToTwoDList(list_data, int(round(col)))


        lm = MyListModel(_twoDLst, col, (thumbWidth, thumbheight), self)
        self.setShowGrid(False)

        self.setWordWrap(True)
        self.setModel(lm)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def keyPressEvent(self, keyevent):
        """ Capture key to exit, next image, previous image,
            on Escape , Key Right and key left respectively.
        """
        event = keyevent.key()
        if event == QtCore.Qt.Key_Escape:
            self.close()

def convertToTwoDList(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window =  MyTableView()
    window.show()
    window.raise_()
    sys.exit(app.exec_())
# python unit-testing
