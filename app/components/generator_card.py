# coding:utf-8
""" 生成器卡片，包含47个CheckBox、日志框和各种操作按钮 """
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QScrollArea

from qfluentwidgets import (
    BodyLabel, PushButton, CheckBox, PlainTextEdit,
    FluentIcon as FIF,
    PrimaryPushButton
)

from app.components.flexible_card import CardBuilder


class GeneratorCard(QWidget):
    """ 生成器卡片类，包含所有需要的组件 """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        
        # 创建核心卡片
        self.card = CardBuilder.createFlexibleCard("配置生成器", self)
        
        # 初始化组件
        self._initWidgets()
        
        # 将卡片添加到主布局
        self.vBoxLayout.addWidget(self.card)
    
    def _initWidgets(self):
        """ 初始化所有组件 """
        
        # 1. 创建47个CheckBox + 1个InitValue CheckBox
        self._createCheckBoxGroup()
        
        # 2. 创建操作按钮组
        self._createActionButtons()
        
        # 3. 创建日志区域
        self._createLogArea()
    
    def _createCheckBoxGroup(self):
        """ 创建47个CheckBox和1个InitValue CheckBox，共48个，排列成矩形 """
        
        # 导入QSizePolicy类
        from PyQt5.QtWidgets import QSizePolicy
        
        # 创建分组标题
        checkBoxTitle = BodyLabel("选择配置项 (48个)", self.card)
        self.card.addWidget(checkBoxTitle)
        
        # 创建滚动区域，用于容纳大量CheckBox
        scrollArea = QScrollArea(self.card)
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setMaximumHeight(400)  # 增加最大高度，更好地显示矩形排列
        scrollArea.setMinimumWidth(1200)  # 增加最大高度，更好地显示矩形排列

        # 滚动区域内容
        scrollContent = QWidget()
        scrollLayout = QVBoxLayout(scrollContent)
        scrollLayout.setSpacing(0)
        scrollLayout.setContentsMargins(0, 0, 0, 0)
        
        # 创建网格布局来排列48个CheckBox（包括InitValue）
        gridLayout = QGridLayout()
        gridLayout.setSpacing(10)  # 调整间距，使布局更紧凑
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setAlignment(Qt.AlignTop)
        
        # 总共48个checkbox，排列成8行6列的矩形
        total_checkboxes = 48
        columns = 8
        
        # 添加47个普通CheckBox
        self.checkBoxes = []
        for i in range(0, total_checkboxes - 1):
            checkbox = CheckBox(f"", scrollContent)
            checkbox.setObjectName(f"checkBox_{i}")
            # 设置checkbox最小宽度，确保能显示完整信息
            checkbox.setFixedWidth(150)  # 可以根据实际需求调整
            checkbox.clicked.connect(self._checkAction)
            # 允许checkbox自动扩展宽度
            checkbox.setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Fixed
            )
            self.checkBoxes.append(checkbox)
            row = i // columns  # 计算行号
            col = i % columns  # 计算列号
            gridLayout.addWidget(checkbox, row, col)
        
        # 添加InitValue CheckBox作为最后一个（第48个）
        self.initValueCheckBox = CheckBox("InitValue", scrollContent)
        # 设置InitValue checkbox最小宽度
        self.initValueCheckBox.setMinimumWidth(150)
        # 允许InitValue checkbox自动扩展宽度
        self.initValueCheckBox.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        # 计算最后一个checkbox的位置（第8行第5列）
        last_row = (total_checkboxes - 1) // columns
        last_col = (total_checkboxes - 1) % columns
        gridLayout.addWidget(self.initValueCheckBox, last_row, last_col)
        
        # 添加网格布局到滚动内容
        scrollLayout.addLayout(gridLayout)
        
        # 设置滚动区域内容
        scrollArea.setWidget(scrollContent)
        
        # 添加滚动区域到卡片
        self.card.addWidget(scrollArea)
    
    def _createActionButtons(self):
        """ 创建操作按钮组 """
        
        # 创建操作按钮布局
        actionLayout = QHBoxLayout()
        actionLayout.setSpacing(10)
        actionLayout.setContentsMargins(0, 0, 0, 0)
        actionLayout.setAlignment(Qt.AlignLeft)
        
        # 一键选择所有47个checkbox的按钮
        self.selectAllBtn = PushButton("全选", self.card, FIF.CHECKBOX)
        self.selectAllBtn.setFixedWidth(100)
        self.selectAllBtn.clicked.connect(self._selectAllCheckBoxes)
        actionLayout.addWidget(self.selectAllBtn)
        
        # 一键清空所有47个checkbox的按钮
        self.clearAllBtn = PushButton("清空", self.card, FIF.DELETE)
        self.clearAllBtn.setFixedWidth(100)
        self.clearAllBtn.clicked.connect(self._clearAllCheckBoxes)
        actionLayout.addWidget(self.clearAllBtn)
        
        # 检查按钮
        self.checkBtn = PushButton("检查", self.card, FIF.CHECKBOX)
        self.checkBtn.setFixedWidth(100)
        self.checkBtn.clicked.connect(self._checkAction)
        actionLayout.addWidget(self.checkBtn)
        
        # 生成按钮1
        self.generateBtn1 = PrimaryPushButton("生成1", self.card, FIF.PLAY_SOLID)
        self.generateBtn1.setFixedWidth(100)
        self.generateBtn1.clicked.connect(self._generateAction1)
        actionLayout.addWidget(self.generateBtn1)
        
        # 生成按钮2
        self.generateBtn2 = PrimaryPushButton("生成2", self.card, FIF.PLAY_SOLID)
        self.generateBtn2.setFixedWidth(100)
        self.generateBtn2.clicked.connect(self._generateAction2)
        actionLayout.addWidget(self.generateBtn2)
        
        # 添加弹簧，使按钮靠左排列
        actionLayout.addStretch(1)
        
        # 添加操作按钮布局到卡片
        self.card.addLayout(actionLayout)
    
    def _createLogArea(self):
        """ 创建日志区域，宽度与卡片宽度一致且完全自适应 """
        
        # 创建日志标题和控制按钮
        logHeaderLayout = QHBoxLayout()
        logHeaderLayout.setSpacing(10)
        logHeaderLayout.setContentsMargins(0, 0, 0, 0)
        
        logTitle = BodyLabel("操作日志", self.card)
        logHeaderLayout.addWidget(logTitle)
        
        # 清空日志按钮
        self.clearLogBtn = PushButton("清空日志", self.card, FIF.DELETE)
        self.clearLogBtn.setFixedWidth(100)
        self.clearLogBtn.clicked.connect(self._clearLog)
        logHeaderLayout.addWidget(self.clearLogBtn)
        
        # 添加弹簧，使标题靠左，按钮靠右
        logHeaderLayout.addStretch(1)
        
        # 添加日志标题布局到卡片
        self.card.addLayout(logHeaderLayout)
        
        # 创建日志文本框
        self.logEdit = PlainTextEdit(self.card)
        self.logEdit.setReadOnly(True)
        
        # 设置日志框最小高度，确保有足够的显示空间
        self.logEdit.setMinimumHeight(400)
        self.logEdit.setMinimumWidth(1200)

        # 设置日志框最大高度，防止过高
        self.logEdit.setMaximumHeight(800)  # 可以根据实际需求调整
        
        self.logEdit.setPlaceholderText("操作日志将显示在这里...")
        
        # 设置日志框大小策略，确保完全自适应
        from PyQt5.QtWidgets import QSizePolicy
        self.logEdit.setSizePolicy(
            QSizePolicy.Expanding,  # 水平方向完全扩展，与卡片宽度一致
            QSizePolicy.Preferred    # 垂直方向优先使用推荐尺寸
        )
        
        # 移除错误的方法调用，PlainTextEdit没有setWidgetResizable方法
        
        # 添加日志文本框到卡片
        self.card.addWidget(self.logEdit)
    
    def setLogSize(self, width=None, height=None):
        """ 设置日志框的宽度和高度
        
        Args:
            width: 日志框宽度，None表示自适应
            height: 日志框高度，None表示自适应
        """
        if width is not None:
            self.logEdit.setFixedWidth(width)
            # 如果设置了固定宽度，调整大小策略
            self.logEdit.setSizePolicy(
                QSizePolicy.Fixed,
                self.logEdit.sizePolicy().verticalPolicy()
            )
        
        if height is not None:
            self.logEdit.setFixedHeight(height)
            # 如果设置了固定高度，调整大小策略
            self.logEdit.setSizePolicy(
                self.logEdit.sizePolicy().horizontalPolicy(),
                QSizePolicy.Fixed
            )
    
    def setLogMinimumSize(self, min_width=None, min_height=None):
        """ 设置日志框的最小宽度和高度
        
        Args:
            min_width: 日志框最小宽度
            min_height: 日志框最小高度
        """
        if min_width is not None:
            self.logEdit.setMinimumWidth(min_width)
        if min_height is not None:
            self.logEdit.setMinimumHeight(min_height)
    
    def setLogMaximumSize(self, max_width=None, max_height=None):
        """ 设置日志框的最大宽度和高度
        
        Args:
            max_width: 日志框最大宽度
            max_height: 日志框最大高度
        """
        if max_width is not None:
            self.logEdit.setMaximumWidth(max_width)
        if max_height is not None:
            self.logEdit.setMaximumHeight(max_height)
    
    def _selectAllCheckBoxes(self):
        """ 一键选择所有48个checkbox（包括InitValue） """
        # 选择InitValue checkbox
        self.initValueCheckBox.setChecked(True)
        # 选择其他47个checkbox
        for checkbox in self.checkBoxes:
            checkbox.setChecked(True)
        self._addLog("已选择所有48个配置项")
    
    def _clearAllCheckBoxes(self):
        """ 一键清空所有48个checkbox（包括InitValue） """
        # 清空InitValue checkbox
        self.initValueCheckBox.setChecked(False)
        # 清空其他47个checkbox
        for checkbox in self.checkBoxes:
            checkbox.setChecked(False)
        self._addLog("已清空所有48个配置项")
    
    def _checkAction(self):
        """ 检查按钮点击事件，统计所有48个checkbox的状态 """
        # 统计普通checkbox选中数量
        selectedCount = sum(1 for checkbox in self.checkBoxes if checkbox.isChecked())
        # 检查InitValue checkbox状态
        initValueChecked = self.initValueCheckBox.isChecked()
        # 总选中数量（包括InitValue）
        totalSelected = selectedCount + (1 if initValueChecked else 0)
        
        logMsg = f"检查结果：共48个配置项，已选择 {totalSelected} 个，InitValue {'已选中' if initValueChecked else '未选中'}"
        self._addLog(logMsg)
    
    def _generateAction1(self):
        """ 生成按钮1点击事件，考虑所有48个checkbox的状态 """
        # 获取选中的普通配置项
        selectedItems = [checkbox.text() for checkbox in self.checkBoxes if checkbox.isChecked()]
        # 获取InitValue状态
        initValueChecked = self.initValueCheckBox.isChecked()
        # 总选中数量
        totalSelected = len(selectedItems) + (1 if initValueChecked else 0)
        
        self._addLog(f"生成1操作开始，共选择 {totalSelected} 个配置项")
        self._addLog(f"InitValue: {'启用' if initValueChecked else '禁用'}")
        if selectedItems:
            self._addLog(f"选中的配置项: {', '.join(selectedItems[:3])}{'...' if len(selectedItems) > 3 else ''}")
        self._addLog("生成1操作完成")
    
    def _generateAction2(self):
        """ 生成按钮2点击事件，考虑所有48个checkbox的状态 """
        # 获取选中的普通配置项
        selectedItems = [checkbox.text() for checkbox in self.checkBoxes if checkbox.isChecked()]
        # 获取InitValue状态
        initValueChecked = self.initValueCheckBox.isChecked()
        # 总选中数量
        totalSelected = len(selectedItems) + (1 if initValueChecked else 0)
        
        self._addLog(f"生成2操作开始，共选择 {totalSelected} 个配置项")
        self._addLog(f"InitValue: {'启用' if initValueChecked else '禁用'}")
        if selectedItems:
            self._addLog(f"选中的配置项: {', '.join(selectedItems[:3])}{'...' if len(selectedItems) > 3 else ''}")
        self._addLog("生成2操作完成")
    
    def _addLog(self, message):
        """ 添加日志信息 """
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logEdit.appendPlainText(f"[{timestamp}] {message}")
        # 自动滚动到底部
        self.logEdit.verticalScrollBar().setValue(self.logEdit.verticalScrollBar().maximum())
    
    def _clearLog(self):
        """ 清空日志 """
        self.logEdit.clear()
        self._addLog("日志已清空")
