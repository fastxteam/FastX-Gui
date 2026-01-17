# coding:utf-8
import os
import re
from typing import List
from PyQt5.QtCore import Qt, QTime

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog

from qfluentwidgets import (IconWidget, BodyLabel, FluentIcon, InfoBarIcon, ComboBox,
                            PrimaryPushButton, LineEdit, GroupHeaderCardWidget, PushButton,
                            CompactSpinBox, SwitchButton, IndicatorPosition, PlainTextEdit,
                            ToolTipFilter, ConfigItem)

from app.common.icon import Logo, PNG
from app.common.config import cfg


class BasicConfigCard(GroupHeaderCardWidget):
    """ Basic config card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(self.tr("Basic Settings"))
        self.mediaParser = None

        self.urlLineEdit = LineEdit()
        self.fileNameLineEdit = LineEdit()
        self.saveFolderButton = PushButton(self.tr("Choose"))
        self.threadCountSpinBox = CompactSpinBox()
        self.streamInfoComboBox = ComboBox()

        self.hintIcon = IconWidget(InfoBarIcon.INFORMATION, self)
        self.hintLabel = BodyLabel(
            self.tr("Click the download button to start downloading") + ' 👉')
        self.downloadButton = PrimaryPushButton(
            self.tr("Download"), self, FluentIcon.PLAY_SOLID)

        self.toolBarLayout = QHBoxLayout()

        self._initWidgets()

    def _initWidgets(self):
        self.setBorderRadius(8)

        self.streamInfoComboBox.setMinimumWidth(120)
        self.streamInfoComboBox.addItem(self.tr("Default"))

        self.downloadButton.setEnabled(False)
        self.hintIcon.setFixedSize(16, 16)

        self.urlLineEdit.setFixedWidth(300)
        self.fileNameLineEdit.setFixedWidth(300)
        self.saveFolderButton.setFixedWidth(120)

        self.urlLineEdit.setClearButtonEnabled(True)
        self.fileNameLineEdit.setClearButtonEnabled(True)

        self.fileNameLineEdit.setPlaceholderText(self.tr("Please enter the name of downloaded file"))
        self.urlLineEdit.setPlaceholderText(self.tr("Please enter the path of m3u8, mpd or txt"))
        self.urlLineEdit.setToolTip(self.tr("The format of each line in the txt file is FileName,URL"))
        self.urlLineEdit.setToolTipDuration(3000)
        self.urlLineEdit.installEventFilter(ToolTipFilter(self.urlLineEdit))

        self._initLayout()
        self._connectSignalToSlot()

    def _initLayout(self):
        # add widget to group
        self.addGroup(
            icon=Logo.GLOBE.icon(),
            title=self.tr("Download URL"),
            content=self.tr("The path of m3u8, mpd or txt file, support drag and drop txt file"),
            widget=self.urlLineEdit
        )
        self.addGroup(
            icon=Logo.FILM.icon(),
            title=self.tr("File Name"),
            content=self.tr("The name of downloaded file"),
            widget=self.fileNameLineEdit
        )
        self.addGroup(
            icon=Logo.PROJECTOR.icon(),
            title=self.tr("Stream Info"),
            content=self.tr("Select the stream to be downloaded"),
            widget=self.streamInfoComboBox
        )
        self.saveFolderGroup = self.addGroup(
            icon=Logo.FOLDER.icon(),
            title=self.tr("Save Folder"),
            content=cfg.get(cfg.saveFolder),
            widget=self.saveFolderButton
        )
        group = self.addGroup(
            icon=Logo.KNOT.icon(),
            title=self.tr("Download Threads"),
            content=self.tr("Set the number of concurrent download threads"),
            widget=self.threadCountSpinBox
        )
        group.setSeparatorVisible(True)

        # add widgets to bottom toolbar
        self.toolBarLayout.setContentsMargins(24, 15, 24, 20)
        self.toolBarLayout.setSpacing(10)
        self.toolBarLayout.addWidget(
            self.hintIcon, 0, Qt.AlignmentFlag.AlignLeft)
        self.toolBarLayout.addWidget(
            self.hintLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.toolBarLayout.addStretch(1)
        self.toolBarLayout.addWidget(
            self.downloadButton, 0, Qt.AlignmentFlag.AlignRight)
        self.toolBarLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.vBoxLayout.addLayout(self.toolBarLayout)

    def _onTextChanged(self):
        url = self.urlLineEdit.text().strip()
        fileName = self.fileNameLineEdit.text()

    def _onUrlChanged(self, url: str):
        url = url.strip()

    def _chooseSaveFolder(self):
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), self.saveFolderGroup.content())

        if folder:
            folder = folder.replace("\\", "/")
            cfg.set(cfg.saveFolder, folder)
            self.saveFolderGroup.setContent(folder)

    def _resetStreamInfo(self):
        self.streamInfoComboBox.clear()
        self.streamInfoComboBox.addItem(self.tr("Default"))

    def _connectSignalToSlot(self):
        self.urlLineEdit.textChanged.connect(self._onUrlChanged)
        self.urlLineEdit.textChanged.connect(self._onTextChanged)
        self.fileNameLineEdit.textChanged.connect(self._onTextChanged)
        self.saveFolderButton.clicked.connect(self._chooseSaveFolder)
        self.threadCountSpinBox.valueChanged.connect(lambda v: cfg.set(cfg.threadCount, v))