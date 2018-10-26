from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import pyqtSignal, pyqtProperty
from PyQt5.QtWidgets import QLabel


class ItemLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ItemLabel, self).__init__(parent)
        self.ADP_filePath = None
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.setFont(QFont("Roman times", 10.5))  ##设置字体
        self._set_color(QColor(255, 255, 255, 255))

    def _set_color(self, col):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), col)
        self.setPalette(palette)

    color = pyqtProperty(QColor, fset=_set_color)

    def enterEvent(self, *args, **kwargs):
        self._set_color(QColor(65, 105, 225, 255))

    def leaveEvent(self, *args, **kwargs):
        self._set_color(QColor(255, 255, 255, 255))

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()

    def setFilePath(self, path):
        self.ADP_filePath = path

    def getFilePath(self):
        return self.ADP_filePath
