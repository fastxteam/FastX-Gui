# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl, QSize, QEventLoop, QTimer
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QSplashScreen
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, SplashScreen)
from qfluentwidgets import FluentIcon as FIF

from app.common.translator import Translator
from .home_interface import HomeInterface
from .setting_interface import SettingInterface


class Widget(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        # 创建启动页面
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))
        # 在创建其他子页面前先显示主界面
        self.show()
        # 创建子界面
        self.createSubInterface()

    def createSubInterface(self):
        # create sub interface
        loop = QEventLoop(self)
        QTimer.singleShot(1000, loop.quit)

        self.homeInterface    = HomeInterface(self)
        self.appInterface     = Widget('Application Interface', self)
        self.projectInterface = Widget('Project Interface', self)
        self.libraryInterface = Widget('Library Interface', self)
        self.logInterface     = Widget('Log Interface', self)
        self.settingInterface = SettingInterface(self)

        self.initNavigation()
        self.initWindow()
        # 隐藏启动页面
        self.splashScreen.finish()

        loop.exec_()

    def initNavigation(self):
        # add navigation items
        t = Translator()
        pos = NavigationItemPosition.TOP
        self.addSubInterface(self.homeInterface, FIF.HOME, t.home, FIF.HOME_FILL, position=pos)
        self.addSubInterface(self.appInterface, FIF.APPLICATION, t.app, position=pos)

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.projectInterface, FIF.CAR, t.project, position=pos)
        self.addSubInterface(self.logInterface, FIF.COMMAND_PROMPT, t.log, position=pos)

        pos = NavigationItemPosition.BOTTOM
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text=t.help,
            onClick=self.showMessageBox,
            selectable=False,
            position=pos,
        )
        self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF, t.library, FIF.LIBRARY_FILL, position=pos)
        self.addSubInterface(self.settingInterface, FIF.SETTING, t.settings, position=pos)

        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        self.resize(1200, 700)
        self.setMinimumWidth(760)
        self.setWindowTitle('福瑞泰克软件中心MCU工具平台')
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()

    def showMessageBox(self):
        w = MessageBox(
            '刘小豪🥰',
            '快歇一歇吧🚀',
            self
        )
        w.yesButton.setText('好的')
        w.cancelButton.setText('好的')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))
