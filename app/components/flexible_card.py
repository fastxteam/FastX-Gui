# coding:utf-8
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy

from qfluentwidgets import (
    SimpleCardWidget, GroupHeaderCardWidget, BodyLabel, TitleLabel,
    FluentIcon, IconWidget
)


class FlexibleCard(SimpleCardWidget):
    """ 可灵活组装组件的卡片类 """

    def __init__(self, title=None, parent=None):
        super().__init__(parent)
        self.setBorderRadius(8)
        
        # 设置卡片的大小策略，确保自动填充父容器宽度
        self.setSizePolicy(
            QSizePolicy.Expanding,  # 水平方向自动扩展
            QSizePolicy.Minimum      # 垂直方向最小大小
        )
        
        # 主布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(12)
        self.mainLayout.setContentsMargins(24, 24, 24, 24)
        self.mainLayout.setAlignment(Qt.AlignTop)
        
        # 标题部分（可选）
        if title:
            self.titleLabel = TitleLabel(title, self)
            self.mainLayout.addWidget(self.titleLabel)
            
            # 添加标题下方的分隔线
            self.mainLayout.addSpacing(8)
        
        # 内容区域布局
        self.contentLayout = QVBoxLayout()
        self.contentLayout.setSpacing(10)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.contentLayout)
        
        # 底部工具栏布局
        self.toolBarLayout = QHBoxLayout()
        self.toolBarLayout.setSpacing(10)
        self.toolBarLayout.setContentsMargins(0, 0, 0, 0)
        self.toolBarLayout.setAlignment(Qt.AlignLeft)
        
        # 底部工具栏是否已添加的标记
        self.toolBarAdded = False
    
    def addWidget(self, widget, alignment=Qt.AlignLeft):
        """ 添加单个组件到卡片 """
        self.contentLayout.addWidget(widget, 0, alignment)
        return self
    
    def addLayout(self, layout):
        """ 添加布局到卡片 """
        self.contentLayout.addLayout(layout)
        return self
    
    def addGroup(self, icon=None, title=None, content=None, widget=None):
        """ 添加一组控件（类似GroupHeaderCardWidget的分组功能） """
        # 创建分组容器
        groupWidget = QWidget(self)
        groupLayout = QVBoxLayout(groupWidget)
        groupLayout.setSpacing(8)
        groupLayout.setContentsMargins(0, 0, 0, 0)
        
        # 标题行
        titleRow = QHBoxLayout()
        titleRow.setSpacing(8)
        titleRow.setContentsMargins(0, 0, 0, 0)
        
        # 添加图标
        if icon:
            iconWidget = IconWidget(icon, groupWidget)
            iconWidget.setFixedSize(16, 16)
            titleRow.addWidget(iconWidget, 0, Qt.AlignVCenter)
        
        # 添加标题
        if title:
            titleLabel = TitleLabel(title, groupWidget)
            titleLabel.setObjectName("groupTitleLabel")
            titleRow.addWidget(titleLabel, 0, Qt.AlignVCenter)
        
        # 添加弹簧
        titleRow.addStretch(1)
        
        # 添加右侧控件
        if widget:
            titleRow.addWidget(widget, 0, Qt.AlignVCenter)
        
        groupLayout.addLayout(titleRow)
        
        # 添加内容描述
        if content:
            contentLabel = BodyLabel(content, groupWidget)
            contentLabel.setObjectName("groupContentLabel")
            groupLayout.addWidget(contentLabel)
        
        self.contentLayout.addWidget(groupWidget)
        return groupWidget
    
    def addSpace(self, space=12):
        """ 添加间距 """
        self.contentLayout.addSpacing(space)
        return self
    
    def addStretch(self):
        """ 添加弹簧 """
        self.contentLayout.addStretch(1)
        return self
    
    def addToolBarWidget(self, widget, alignment=Qt.AlignLeft):
        """ 添加组件到底部工具栏 """
        # 如果工具栏尚未添加，先添加
        if not self.toolBarAdded:
            self.mainLayout.addSpacing(16)
            self.mainLayout.addLayout(self.toolBarLayout)
            self.toolBarAdded = True
        
        self.toolBarLayout.addWidget(widget, 0, alignment)
        return self
    
    def addToolBarLayout(self, layout):
        """ 添加布局到底部工具栏 """
        # 如果工具栏尚未添加，先添加
        if not self.toolBarAdded:
            self.mainLayout.addSpacing(16)
            self.mainLayout.addLayout(self.toolBarLayout)
            self.toolBarAdded = True
        
        self.toolBarLayout.addLayout(layout)
        return self
    
    def addToolBarStretch(self):
        """ 添加弹簧到底部工具栏 """
        # 如果工具栏尚未添加，先添加
        if not self.toolBarAdded:
            self.mainLayout.addSpacing(16)
            self.mainLayout.addLayout(self.toolBarLayout)
            self.toolBarAdded = True
        
        self.toolBarLayout.addStretch(1)
        return self
    
    def enableTransparentBackground(self):
        """ 启用透明背景 """
        self.setProperty("transparent", True)
        return self


class ConfigCard(GroupHeaderCardWidget):
    """ 配置类型卡片，继承自GroupHeaderCardWidget，提供更灵活的配置项添加方式 """
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setTitle(title)
        self.setBorderRadius(8)
        
        # 设置卡片的大小策略，确保自动填充父容器宽度
        self.setSizePolicy(
            QSizePolicy.Expanding,  # 水平方向自动扩展
            QSizePolicy.Minimum      # 垂直方向最小大小
        )
        
        # 底部工具栏布局
        self.toolBarLayout = QHBoxLayout()
        self.toolBarLayout.setSpacing(10)
        self.toolBarLayout.setContentsMargins(24, 15, 24, 20)
        self.toolBarLayout.setAlignment(Qt.AlignVCenter)
        
        # 底部工具栏是否已添加的标记
        self.toolBarAdded = False
    
    def addToolBarWidget(self, widget, alignment=Qt.AlignLeft):
        """ 添加组件到底部工具栏 """
        # 如果工具栏尚未添加，先添加
        if not self.toolBarAdded:
            self.vBoxLayout.addLayout(self.toolBarLayout)
            self.toolBarAdded = True
        
        self.toolBarLayout.addWidget(widget, 0, alignment)
        return self
    
    def addToolBarStretch(self):
        """ 添加弹簧到底部工具栏 """
        # 如果工具栏尚未添加，先添加
        if not self.toolBarAdded:
            self.vBoxLayout.addLayout(self.toolBarLayout)
            self.toolBarAdded = True
        
        self.toolBarLayout.addStretch(1)
        return self
    
    def addToolBarSpacing(self, space=10):
        """ 添加间距到底部工具栏 """
        # 如果工具栏尚未添加，先添加
        if not self.toolBarAdded:
            self.vBoxLayout.addLayout(self.toolBarLayout)
            self.toolBarAdded = True
        
        self.toolBarLayout.addSpacing(space)
        return self


class CardBuilder:
    """ 卡片构建器，用于更便捷地创建卡片 """
    
    @staticmethod
    def createFlexibleCard(title=None, parent=None):
        """ 创建灵活组装卡片 """
        return FlexibleCard(title, parent)
    
    @staticmethod
    def createConfigCard(title, parent=None):
        """ 创建配置卡片 """
        return ConfigCard(title, parent)
    
    @staticmethod
    def createInfoCard(title, description=None, parent=None):
        """ 创建信息展示卡片 """
        card = FlexibleCard(title, parent)
        if description:
            from qfluentwidgets import BodyLabel
            descLabel = BodyLabel(description, card)
            descLabel.setWordWrap(True)
            card.addWidget(descLabel)
        return card
    
    @staticmethod
    def createActionCard(title, actions=None, parent=None):
        """ 创建操作卡片，包含多个按钮 """
        card = FlexibleCard(title, parent)
        if actions:
            from qfluentwidgets import PushButton
            actionLayout = QHBoxLayout()
            actionLayout.setSpacing(10)
            for action in actions:
                btn = PushButton(action['text'], card, action.get('icon'))
                if 'callback' in action:
                    btn.clicked.connect(action['callback'])
                if 'width' in action:
                    btn.setFixedWidth(action['width'])
                actionLayout.addWidget(btn)
            card.addLayout(actionLayout)
        return card
