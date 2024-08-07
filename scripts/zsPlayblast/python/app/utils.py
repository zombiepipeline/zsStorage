import os
import sys

from sgtk.platform.qt import QtCore, QtGui


class Utils:

    @staticmethod
    def loadImage(filename):
        path = os.path.dirname(__file__)
        return os.path.join(path, '..\\', '..\\', 'resources', '{0}.png'.format(filename))

    @staticmethod
    def loadIcon(filename):
        path = os.path.dirname(__file__)
        icon_path = os.path.join(path, '..\\', '..\\', 'resources', '{0}.png'.format(filename))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        return icon