# coding:utf-8
from pathlib import Path
from typing import List
from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtGui import QDropEvent, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGraphicsDropShadowEffect

from qfluentwidgets import ScrollArea, InfoBar, InfoBarPosition, PushButton, SubtitleLabel, setFont
from qfluentwidgets import FluentIcon as FIF
from app.components.info_card import AppInfoCard
from ..components.config_card import BasicConfigCard
from app.components.flexible_card import CardBuilder
from app.components.card_example import CardExample
from app.components.generator_card import GeneratorCard



class FuncInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = QWidget(self)

        self.funcInfoCard = AppInfoCard()
        self.basicSettingCard = BasicConfigCard()

        self.basicSettingCard.chooseMappingTableButton.setIcon(FIF.DOCUMENT)
        self.basicSettingCard.chooseDataTypeButton.setIcon(FIF.DOCUMENT)
        self.basicSettingCard.chooseInterfaceButton.setIcon(FIF.DOCUMENT)
        self.basicSettingCard.outputFolderButton.setIcon(FIF.FOLDER)

        self.vBoxLayout = QVBoxLayout(self.view)

        self._initWidget()

    def _initWidget(self):
        self.setWidget(self.view)
        self.setAcceptDrops(True)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 10)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # 添加原有卡片
        self.vBoxLayout.addWidget(self.funcInfoCard, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.basicSettingCard, 0, Qt.AlignmentFlag.AlignTop)
        
        # 添加可组装卡片系统示例
        self.vBoxLayout.addSpacing(20)
        
        # 创建示例标题
        exampleTitle = SubtitleLabel("可组装卡片系统示例", self.view)
        setFont(exampleTitle, 18)
        self.vBoxLayout.addWidget(exampleTitle)
        
        # 添加卡片示例
        self.cardExample = CardExample(self.view)
        self.vBoxLayout.addWidget(self.cardExample, 0, Qt.AlignTop)
        
        # 创建自定义配置卡片
        self._createCustomConfigCard()
        
        # 添加生成器卡片
        self.vBoxLayout.addSpacing(20)
        
        # 创建生成器卡片标题
        generatorTitle = SubtitleLabel("生成器卡片示例", self.view)
        setFont(generatorTitle, 18)
        self.vBoxLayout.addWidget(generatorTitle)
        
        # 添加生成器卡片
        self.generatorCard = GeneratorCard(self.view)
        self.vBoxLayout.addWidget(self.generatorCard, 0, Qt.AlignTop)
        
        self.resize(780, 800)
        self.setObjectName("packageInterface")
        self.enableTransparentBackground()
        # self._connectSignalToSlot()
    
    def _createCustomConfigCard(self):
        """ 使用可组装卡片系统创建自定义配置卡片 """
        from qfluentwidgets import ComboBox, LineEdit, SwitchButton, PrimaryPushButton
        
        # 创建配置卡片
        configCard = CardBuilder.createConfigCard("可组装配置卡片示例", self.view)
        
        # 添加各种配置项
        
        # 1. 工具引擎选择
        engineComboBox = ComboBox()
        engineComboBox.addItem("L2 Func", userData="FUNC")
        engineComboBox.addItem("Ipc Com", userData="IPC")
        engineComboBox.addItem("Srp Com", userData="SRP")
        configCard.addGroup(
            icon=FIF.SETTING,
            title="工具引擎",
            content="选择要使用的工具引擎",
            widget=engineComboBox
        )
        
        # 2. 映射表路径
        configCard.addGroup(
            icon=FIF.FOLDER,
            title="映射表路径",
            content="请选择映射表文件",
            widget=PushButton("浏览", self.view, FIF.FOLDER)
        )
        
        # 3. 输出文件夹
        configCard.addGroup(
            icon=FIF.SAVE,
            title="输出文件夹",
            content="请选择输出文件夹",
            widget=PushButton("选择", self.view, FIF.SAVE)
        )
        
        # 4. 高级选项开关
        configCard.addGroup(
            icon=FIF.CHECKBOX,
            title="高级选项",
            content="启用高级配置选项",
            widget=SwitchButton(self.view)
        )
        
        # 5. 日志级别选择
        logComboBox = ComboBox()
        logComboBox.addItem("调试", userData="DEBUG")
        logComboBox.addItem("信息", userData="INFO")
        logComboBox.addItem("警告", userData="WARNING")
        logComboBox.addItem("错误", userData="ERROR")
        configCard.addGroup(
            icon=FIF.INFO,
            title="日志级别",
            content="设置日志输出级别",
            widget=logComboBox
        )
        
        # 添加底部操作按钮
        configCard.addToolBarWidget(PushButton("重置", self.view, FIF.SYNC))
        configCard.addToolBarWidget(PushButton("保存", self.view, FIF.SAVE))
        configCard.addToolBarStretch()
        configCard.addToolBarWidget(PrimaryPushButton("执行", self.view, FIF.PLAY_SOLID))
        
        self.vBoxLayout.addWidget(configCard, 0, Qt.AlignTop)
        # self._connectSignalToSlot()
        
    def _createCustomConfigCard(self):
        """ 使用可组装卡片系统创建自定义配置卡片 """
        from qfluentwidgets import ComboBox, LineEdit, SwitchButton, PrimaryPushButton
        
        # 创建配置卡片
        configCard = CardBuilder.createConfigCard("可组装配置卡片示例", self.view)
        
        # 添加各种配置项
        
        # 1. 工具引擎选择
        engineComboBox = ComboBox()
        engineComboBox.addItem("L2 Func", userData="FUNC")
        engineComboBox.addItem("Ipc Com", userData="IPC")
        engineComboBox.addItem("Srp Com", userData="SRP")
        configCard.addGroup(
            icon=FIF.SETTING,
            title="工具引擎",
            content="选择要使用的工具引擎",
            widget=engineComboBox
        )
        
        # 2. 映射表路径
        configCard.addGroup(
            icon=FIF.FOLDER,
            title="映射表路径",
            content="请选择映射表文件",
            widget=PushButton("浏览", self.view, FIF.FOLDER)
        )
        
        # 3. 输出文件夹
        configCard.addGroup(
            icon=FIF.SAVE,
            title="输出文件夹",
            content="请选择输出文件夹",
            widget=PushButton("选择", self.view, FIF.SAVE)
        )
        
        # 4. 高级选项开关
        configCard.addGroup(
            icon=FIF.CHECKBOX,
            title="高级选项",
            content="启用高级配置选项",
            widget=SwitchButton(self.view)
        )
        
        # 5. 日志级别选择
        logComboBox = ComboBox()
        logComboBox.addItem("调试", userData="DEBUG")
        logComboBox.addItem("信息", userData="INFO")
        logComboBox.addItem("警告", userData="WARNING")
        logComboBox.addItem("错误", userData="ERROR")
        configCard.addGroup(
            icon=FIF.INFO,
            title="日志级别",
            content="设置日志输出级别",
            widget=logComboBox
        )
        
        # 添加底部操作按钮
        configCard.addToolBarWidget(PushButton("重置", self.view, FIF.SYNC))
        configCard.addToolBarWidget(PushButton("保存", self.view, FIF.SAVE))
        configCard.addToolBarStretch()
        configCard.addToolBarWidget(PrimaryPushButton("执行", self.view, FIF.PLAY_SOLID))
        
        self.vBoxLayout.addWidget(configCard, 0, Qt.AlignmentFlag.AlignTop)

    def _onDownloadButtonClicked(self):
        pass

    def _connectSignalToSlot(self):
        self.basicSettingCard.exeButton.clicked.connect(self._onDownloadButtonClicked)