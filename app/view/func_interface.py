# coding:utf-8
from pathlib import Path
from typing import List
from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtGui import QDropEvent, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGraphicsDropShadowEffect, QLabel

from qfluentwidgets import ScrollArea, InfoBar, InfoBarPosition, PushButton, SubtitleLabel, setFont, MessageBox, \
    SettingCardGroup
from qfluentwidgets import FluentIcon as FIF

from app.components.info_card import AppInfoCard
from app.components.config_card import BasicConfigCard
from app.components.generator_card import GeneratorCard
from app.card.autoplot_setting_card import AutoPlotSettingCard
from app.common.style_sheet import StyleSheet
from app.components.flexible_card import CardBuilder
from app.components.card_example import CardExample

class FuncInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.funcInfoCard = AppInfoCard()
        self.basicSettingCard = BasicConfigCard()
        self.generatorCard = GeneratorCard(self.view)
        self.automaticPlotCard = AutoPlotSettingCard(
            icon=FIF.IMAGE_EXPORT,
            title=self.tr("Select SWCs"),
            content="Select SWCs of which should be generate by tools"
        )

        self._initWidget()

    def _initWidget(self):
        self.setWidget(self.view)
        self.setAcceptDrops(True)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.vBoxLayout.setSpacing(20)
        self.vBoxLayout.setContentsMargins(10, 0, 10, 10)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.vBoxLayout.addWidget(self.funcInfoCard, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.automaticPlotCard, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.basicSettingCard, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.generatorCard, 0, Qt.AlignmentFlag.AlignTop)
        
        self.resize(780, 800)
        self.__initLayout()
        self.__setQss()
        self._connectSignalToSlot()

    def __initLayout(self):
        pass

    def __setQss(self):
        """ set style sheet """
        # initialize style sheet
        self.setObjectName('rteInterface')
        self.view.setObjectName('scrollWidget')
        self.vBoxLayout.setObjectName('vBoxLayout')
        self.enableTransparentBackground()
        StyleSheet.RTE_INTERFACE.apply(self)

    def _showMessageDialog(self):
        title = self.tr('This is a message dialog with mask')
        content = self.tr(
            "If the content of the message box is veeeeeeeeeeeeeeeeeeeeeeeeeery long, it will automatically wrap like this.")
        w = MessageBox(title, content, self.window())
        w.setContentCopyable(True)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')

    def _connectSignalToSlot(self):
        self.basicSettingCard.exeButton.clicked.connect(self._showMessageDialog)