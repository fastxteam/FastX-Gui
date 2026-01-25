# coding:utf-8
from PyQt5 import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QLabel


class TypewriterLabel(QLabel):
    def __init__(self, parent=None):
        super(TypewriterLabel, self).__init__(parent)
        self.texts = ["Welcome to use FastXGui. "
                      "\nThis software is currently in the initial testing stage."
                      "\nThe only open function is FastRte. "
                      "\nMore functions will be developed in the future.💕"]
        self.index = 0
        self.char_index = 0
        self.cursor_visible = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(90)

    def update_label(self):
        if self.char_index > len(self.texts[self.index]):
            if self.index + 1 >= len(self.texts):
                self.timer.stop()
                return
            # 如果已经打印完一行，就打印下一行
            self.index = (self.index + 1) % len(self.texts)
            self.char_index = 0
        text = self.texts[self.index][:self.char_index]
        if self.cursor_visible:
            text += "|"
        else:
            text += " "
        self.setText(text)
        self.cursor_visible = not self.cursor_visible
        self.char_index += 1