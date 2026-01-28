# coding:utf-8
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QApplication, QMainWindow
from qfluentwidgets import FluentIcon as FIF, ScrollArea, IconWidget, CaptionLabel, BodyLabel, TransparentToolButton, \
    PushButton, TransparentToggleToolButton, SwitchButton, VerticalSeparator, SearchLineEdit, ComboBox, StrongBodyLabel, \
    setTheme, setThemeColor
import datetime
import sys
from enum import Enum

from rich.theme import Theme
from app.common.style_sheet import StyleSheet


class LogLevel(Enum):
    """日志级别枚举"""
    INFO = 0
    WARNING = 1
    ERROR = 2
    DEBUG = 3
    SUCCESS = 4


class LogItem(QWidget):
    """日志条目组件"""

    def __init__(self, message: str, level: LogLevel, parent=None):
        super().__init__(parent)
        self.message = message
        self.level = level
        self.timestamp = datetime.datetime.now()

        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setObjectName("LogItem")
        StyleSheet.LOG_INTERFACE.apply(self)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        # 级别图标
        icon = IconWidget(LogInterface.LEVEL_CONFIG[self.level]['icon'])
        icon.setFixedSize(20, 20)

        # 时间标签
        time_str = self.timestamp.strftime("%H:%M:%S")
        time_label = CaptionLabel(time_str)
        time_label.setFixedWidth(70)
        time_label.setTextColor("#888888")

        # 消息标签
        message_label = BodyLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setTextColor("#333333")

        layout.addWidget(icon)
        layout.addWidget(time_label)
        layout.addWidget(message_label, 1)

        # 操作按钮
        copy_btn = TransparentToolButton(FIF.COPY)
        copy_btn.setFixedSize(24, 24)
        copy_btn.setIconSize(QSize(14, 14))
        copy_btn.clicked.connect(self.copy_message)

        layout.addWidget(copy_btn)

    def copy_message(self):
        """复制日志消息"""
        clipboard = QApplication.clipboard()
        full_text = f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.message}"
        clipboard.setText(full_text)


class LogInterface(ScrollArea):
    """日志界面 - 使用PyQt-Fluent-Widgets设计"""

    # 日志级别配置
    LEVEL_CONFIG = {
        LogLevel.INFO: {
            'name': '信息',
            'color': '#00aaff',
            'icon': FIF.INFO,
            'bg_color': '#e6f7ff'
        },
        LogLevel.WARNING: {
            'name': '警告',
            'color': '#ff9800',
            'icon': FIF.QUESTION,
            'bg_color': '#fff7e6'
        },
        LogLevel.ERROR: {
            'name': '错误',
            'color': '#f44336',
            'icon': FIF.CLOSE,
            'bg_color': '#ffe6e6'
        },
        LogLevel.DEBUG: {
            'name': '调试',
            'color': '#9c27b0',
            'icon': FIF.CODE,
            'bg_color': '#f3e6ff'
        },
        LogLevel.SUCCESS: {
            'name': '成功',
            'color': '#4caf50',
            'icon': FIF.COMPLETED,
            'bg_color': '#e6ffe6'
        }
    }

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.view = QWidget(self)
        self.title = title
        self.log_count = 0
        self.max_logs = 1000  # 最大日志数量
        self.filter_level = None  # 当前过滤级别

        """初始化界面"""
        self.__initLayout()
        self.create_title_bar() # 创建标题栏
        self.create_tool_bar()  # 创建工具栏
        self.create_search_box()# 创建搜索框
        self.create_stats_bar() # 创建统计信息栏
        self.create_log_list()  # 创建日志列表
        self.create_bottom_bar()# 创建底部操作栏
        self.__initWidget()
        self.setup_connections()
        
        # 添加一些示例日志
        self.add_log("系统启动成功", LogLevel.SUCCESS)
        self.add_log("正在加载配置文件...", LogLevel.INFO)
        self.add_log("配置文件加载完成", LogLevel.SUCCESS)
        self.add_log("日志系统初始化完成", LogLevel.INFO)

    def __initWidget(self):
        self.setObjectName("logInterface")
        self.view.setObjectName('view')
        StyleSheet.LOG_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

    def __initLayout(self):
        # 顶层布局
        self.Layout = QHBoxLayout(self.view)
        self.Layout.setContentsMargins(0, 48, 0, 0)
        # 主布局
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)
        self.Layout.addLayout(self.main_layout)

    def create_title_bar(self):
        """创建标题栏"""
        # 创建标题栏
        self.title_layout = QHBoxLayout()
        # 标题
        self.title_label = StrongBodyLabel("日志中心")
        self.title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        # 副标题
        self.subtitle_label = CaptionLabel("实时记录系统运行状态")
        self.subtitle_label.setTextColor("#666666")
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addSpacing(10)
        self.title_layout.addWidget(self.subtitle_label)
        self.title_layout.addStretch()
        self.main_layout.addLayout(self.title_layout)

    def create_tool_bar(self):
        """创建工具栏"""
        # 创建菜单栏
        self.toolbar = QHBoxLayout()
        self.toolbar.setSpacing(10)
        # 清空按钮
        self.clear_btn = TransparentToolButton(FIF.DELETE)
        self.clear_btn.setToolTip("清空日志")
        self.clear_btn.setFixedSize(32, 32)
        # 导出按钮
        self.export_btn = TransparentToolButton(FIF.SAVE)
        self.export_btn.setToolTip("导出日志")
        self.export_btn.setFixedSize(32, 32)
        # 级别过滤按钮组
        self.filter_buttons = {}
        for level in LogLevel:
            btn = TransparentToggleToolButton(self.LEVEL_CONFIG[level]['icon'])
            btn.setToolTip(f"仅显示{self.LEVEL_CONFIG[level]['name']}")
            btn.setFixedSize(32, 32)
            btn.setProperty('level', level.value)
            self.filter_buttons[level] = btn
        # 自动滚动开关
        self.auto_scroll = SwitchButton()
        self.auto_scroll.setChecked(True)
        self.auto_scroll.setText("自动滚动")
        # 分隔符
        self.separator = VerticalSeparator()
        self.toolbar.addWidget(self.clear_btn)
        self.toolbar.addWidget(self.export_btn)
        self.toolbar.addWidget(self.separator)
        for level in LogLevel:
            self.toolbar.addWidget(self.filter_buttons[level])
        self.toolbar.addStretch()
        self.toolbar.addWidget(self.auto_scroll)
        self.main_layout.addLayout(self.toolbar)

    def create_search_box(self):
        """创建搜索框"""
        # 创建搜索栏
        self.search_layout = QHBoxLayout()
        self.search_layout.setSpacing(10)
        # 搜索框
        self.search_box = SearchLineEdit()
        self.search_box.setPlaceholderText("搜索日志内容...")
        self.search_box.setFixedHeight(32)
        # 时间范围选择
        self.time_filter = ComboBox()
        self.time_filter.setFixedWidth(150)
        self.time_filter.addItems(["全部时间", "最近1小时", "最近24小时", "最近7天"])
        self.search_layout.addWidget(self.search_box)
        self.search_layout.addWidget(self.time_filter)
        self.main_layout.addLayout(self.search_layout)
    def create_stats_bar(self):
        """创建统计信息栏"""
        self.stats_widget = QWidget()
        self.stats_layout = QHBoxLayout(self.stats_widget)
        self.stats_layout.setContentsMargins(10, 5, 10, 5)
        self.stats_layout.setSpacing(15)
        self.stats_labels = {}
        for level in LogLevel:
            frame = QFrame()
            frame.setObjectName("StatsFrame")
            frame_layout = QHBoxLayout(frame)
            frame_layout.setContentsMargins(10, 5, 10, 5)
            frame_layout.setSpacing(5)
            # 图标
            icon = IconWidget(self.LEVEL_CONFIG[level]['icon'])
            icon.setFixedSize(16, 16)
            # 统计标签
            label = BodyLabel("0")
            label.setStyleSheet(f"color: {self.LEVEL_CONFIG[level]['color']}; font-weight: bold;")
            # 名称标签
            name_label = CaptionLabel(self.LEVEL_CONFIG[level]['name'])
            name_label.setTextColor("#666666")
            frame_layout.addWidget(icon)
            frame_layout.addWidget(label)
            frame_layout.addWidget(name_label)
            self.stats_labels[level] = label
            self.stats_layout.addWidget(frame)
        self.stats_layout.addStretch()
        self.main_layout.addWidget(self.stats_widget)

    def create_log_list(self):
        """创建日志列表"""
        # 创建列表容器
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.setContentsMargins(0, 0, 0, 0)

        # 日志列表容器
        self.log_container = QWidget()
        self.log_container.setObjectName("LogContainer")
        self.log_layout = QVBoxLayout(self.log_container)
        self.log_layout.setAlignment(Qt.AlignTop)
        self.log_layout.setSpacing(2)
        self.log_layout.setContentsMargins(0, 5, 5, 5)

        # 滚动区域
        self.scroll_widget = ScrollArea()
        self.scroll_widget.setWidgetResizable(True)
        self.scroll_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_widget.setWidget(self.log_container)

        list_layout.addWidget(self.scroll_widget)
        self.main_layout.addWidget(list_widget, 1)

    def create_bottom_bar(self):
        """创建底部操作栏"""
        bottom_bar = QHBoxLayout()
        bottom_bar.setSpacing(10)

        # 日志数量显示
        self.count_label = CaptionLabel("日志数量: 0")

        # 操作按钮
        self.copy_selected_btn = PushButton("复制选中", self)
        self.copy_selected_btn.setIcon(FIF.COPY)
        self.copy_selected_btn.setEnabled(False)

        self.save_all_btn = PushButton("保存全部", self)
        self.save_all_btn.setIcon(FIF.SAVE)

        bottom_bar.addWidget(self.count_label)
        bottom_bar.addStretch()
        bottom_bar.addWidget(self.copy_selected_btn)
        bottom_bar.addWidget(self.save_all_btn)

        self.main_layout.addLayout(bottom_bar)

    def setup_connections(self):
        """设置信号连接"""
        self.clear_btn.clicked.connect(self.clear_logs)
        self.export_btn.clicked.connect(self.export_logs)
        self.search_box.textChanged.connect(self.filter_logs)
        self.time_filter.currentTextChanged.connect(self.filter_logs)

        for btn in self.filter_buttons.values():
            btn.clicked.connect(self.on_filter_clicked)

        self.copy_selected_btn.clicked.connect(self.copy_selected)
        self.save_all_btn.clicked.connect(self.save_all_logs)

    def add_log(self, message: str, level: LogLevel = LogLevel.INFO):
        """添加日志条目"""
        if self.log_count >= self.max_logs:
            # 移除最早的日志
            oldest_item = self.log_layout.takeAt(0)
            if oldest_item and oldest_item.widget():
                oldest_item.widget().deleteLater()
                self.log_count -= 1

        # 创建日志条目
        log_item = LogItem(message, level, self)
        self.log_layout.addWidget(log_item)

        # 更新统计
        self.update_stats(level, 1)
        self.log_count += 1
        self.count_label.setText(f"日志数量: {self.log_count}")

        # 自动滚动
        if self.auto_scroll.isChecked():
            QTimer.singleShot(10, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        """滚动到底部"""
        scrollbar = self.scroll_widget.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def update_stats(self, level: LogLevel, delta: int):
        """更新统计信息"""
        current = int(self.stats_labels[level].text())
        self.stats_labels[level].setText(str(current + delta))

    def clear_logs(self):
        """清空所有日志"""
        # 清空布局中的所有部件
        while self.log_layout.count():
            item = self.log_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

        # 重置统计
        for label in self.stats_labels.values():
            label.setText("0")

        self.log_count = 0
        self.count_label.setText("日志数量: 0")

    def filter_logs(self):
        """过滤日志"""
        search_text = self.search_box.text().lower()
        time_filter = self.time_filter.currentText()

        for i in range(self.log_layout.count()):
            item = self.log_layout.takeAt(0)
            if item and item.widget():
                log_item = item.widget()
                visible = True

                # 文本过滤
                if search_text and search_text not in log_item.message.lower():
                    visible = False

                # 级别过滤
                if self.filter_level is not None and log_item.level != self.filter_level:
                    visible = False

                self.log_layout.addWidget(log_item)
                log_item.setVisible(visible)

    def on_filter_clicked(self):
        """处理过滤器点击"""
        sender = self.sender()
        if sender.isChecked():
            self.filter_level = LogLevel(sender.property('level'))
        else:
            self.filter_level = None

        self.filter_logs()

    def export_logs(self):
        """导出日志"""
        # 实现导出逻辑
        pass

    def copy_selected(self):
        """复制选中的日志"""
        # 实现复制逻辑
        pass

    def save_all_logs(self):
        """保存所有日志"""
        # 实现保存逻辑
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置Fluent样式
    # setTheme(Theme.LIGHT)
    setThemeColor('#0078d4')

    window = QMainWindow()
    window.setWindowTitle("日志界面演示")
    window.resize(1000, 700)

    # 创建日志界面
    log_interface = LogInterface("系统日志", window)

    window.setCentralWidget(log_interface)
    window.show()
    sys.exit(app.exec_())