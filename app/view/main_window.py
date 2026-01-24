# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl, QSize, QEventLoop, QTimer, QDateTime
from PyQt5.QtGui import QIcon, QDesktopServices, QFont, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QSplashScreen, QLabel, QStatusBar, QFrame
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow, isDarkTheme,
                            NavigationAvatarWidget, SearchLineEdit, qrouter, SubtitleLabel, setFont, SplashScreen,
                            IndeterminateProgressBar, ProgressBar, PushButton, FluentIcon as FIF, InfoBar,
                            InfoBarPosition)
from qframelesswindow import FramelessWindow, TitleBar

from app.view.home_interface import HomeInterface
from app.view.setting_interface import SettingInterface
from app.view.app_interface import AppInterface
from app.view.log_interface import LogInterface
from app.view.rte_interface import RteInterface
from app.view.func_interface import FuncInterface
from app.view.library_interface import LibraryViewInterface

from app.common.icon import Icon
from app.common.translator import Translator
from app.common.style_sheet import StyleSheet
from app.common.signal_bus import signalBus
from app.common.config import cfg
from app.common import resource

from app.common.setting import VERSION


class Widget(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class CustomTitleBar(TitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.hBoxLayout.removeWidget(self.closeBtn)

        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertSpacing(0, 20)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.titleLabel.setObjectName('titleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)

        # add search line edit
        self.searchLineEdit = SearchLineEdit(self)
        self.searchLineEdit.setObjectName('searchLineEdit')
        self.searchLineEdit.setPlaceholderText('搜索应用、脚本、工具、设置等')
        self.searchLineEdit.setFixedWidth(400)
        self.searchLineEdit.setClearButtonEnabled(True)

        self.vBoxLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignTop)
        self.buttonLayout.addWidget(self.minBtn)
        self.buttonLayout.addWidget(self.maxBtn)
        self.buttonLayout.addWidget(self.closeBtn)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addStretch(1)
        self.hBoxLayout.addLayout(self.vBoxLayout, 0)

    def setTitle(self, title):
        StyleSheet.MAIN_WINDOW.apply(self)
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))

    def resizeEvent(self, e):
        self.searchLineEdit.move((self.width() - self.searchLineEdit.width()) // 2, 8)

class MainWindow(MSFluentWindow):
    def __init__(self):
        # 先调用父类初始化
        super().__init__()
        self.initWindow()

        # 创建子界面
        self.homeInterface = HomeInterface(self)
        self.appInterface = AppInterface(self)
        self.projectInterface = RteInterface(self)
        self.funcInterface = FuncInterface(self)
        self.libraryInterface = LibraryViewInterface(self)
        self.logInterface = LogInterface(self)
        self.settingInterface = SettingInterface(self)

        # 创建信号连接到槽
        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)

    def initNavigation(self):
        # add navigation items
        t = Translator()
        pos = NavigationItemPosition.TOP
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr("Home"), FIF.HOME_FILL, position=pos, isTransparent=True)
        self.addSubInterface(self.appInterface , FIF.APPLICATION, self.tr("App"), position=pos, isTransparent=False)

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.projectInterface, FIF.CAR, self.tr("Project"), position=pos, isTransparent=False)
        self.addSubInterface(self.logInterface, FIF.COMMAND_PROMPT, self.tr("Log"), position=pos, isTransparent=False)
        self.addSubInterface(self.funcInterface, FIF.CALORIES, self.tr("Rte"), position=pos, isTransparent=True)
        self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF, self.tr("Library"), FIF.LIBRARY_FILL, position=pos, isTransparent=False)

        pos = NavigationItemPosition.BOTTOM
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text= self.tr("Help"),
            onClick=self.showMessageBox,
            selectable=False,
            position=pos,
        )
        self.addSubInterface(self.settingInterface, Icon.SETTINGS, self.tr('Settings'), Icon.SETTINGS_FILLED, position=pos, isTransparent=False)
        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())
        self.splashScreen.finish()

    def initWindow(self):
        self.resize(1200, 860)
        self.setMinimumWidth(1200)
        self.setMaximumWidth(1200)
        # 设置自定义标题栏
        self.setTitleBar(CustomTitleBar(self))
        self.titleBar.raise_()
        # 调整布局边距以适应标题栏高度
        self.hBoxLayout.setContentsMargins(0, 48, 0, 0)
        # 设置图标,标题
        self.setWindowIcon(QIcon(':/app/images/logo-m.png'))
        self.setWindowTitle(f'FastXGuI {VERSION}')
        self.__setQss()

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()
        # desktop show
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def __setQss(self):
        """ set style sheet """
        # initialize style sheet
        self.setObjectName('mainWindow')
        StyleSheet.MAIN_WINDOW.apply(self)
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

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