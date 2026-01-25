from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath, QLinearGradient, QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGraphicsDropShadowEffect
from qfluentwidgets import TextEdit, SwitchButton, IndicatorPosition, PushButton, TitleLabel, BodyLabel, \
    PrimaryPushSettingCard, SubtitleLabel, ScrollArea, isDarkTheme, InfoBar, InfoBarIcon, InfoBarPosition
from qfluentwidgets import FluentIcon as FIF
from PIL import Image
import numpy as np

from app.components.link_card import LinkCardView
from app.common.style_sheet import StyleSheet
from app.components.type_writer import TypewriterLabel


class BannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(320)
        self.setMaximumHeight(320)

        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel(f'', self)
        self.galleryLabel.setStyleSheet("color: white;font-size: 30px; font-weight: 600;")
        # self.banner = QPixmap('./app/resource/images/bg37.jpg')
        self.img = Image.open("./app/resource/images/bg37.jpg")
        self.banner = None
        self.path = None

        # 创建阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)  # 阴影模糊半径
        shadow.setColor(Qt.black)  # 阴影颜色
        shadow.setOffset(1.2, 1.2)     # 阴影偏移量

        # 将阴影效果应用于小部件
        self.galleryLabel.setGraphicsEffect(shadow)
        self.galleryLabel.setObjectName('galleryLabel')

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        if not self.banner or not self.path:
            image_height = self.img.width * self.height() // self.width()
            crop_area = (0, 0, self.img.width, image_height)  # (left, upper, right, lower)
            cropped_img = self.img.crop(crop_area)
            img_data = np.array(cropped_img)  # Convert PIL Image to numpy array
            height, width, channels = img_data.shape
            bytes_per_line = channels * width
            self.banner = QImage(img_data.data, width, height, bytes_per_line, QImage.Format_RGB888)

            path = QPainterPath()
            path.addRoundedRect(0, 0, width + 50, height + 50, 10, 10)  # 10 is the radius for corners
            self.path = path.simplified()

        painter.setClipPath(self.path)
        painter.drawImage(self.rect(), self.banner)


class HomeInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.banner = BannerWidget(self.view)
        self.intro = TypewriterLabel(self.view)
        self.__initWidget()
        self.__initLayout()
        self.loadSamples()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName(f"homeInterface")
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

    def __initLayout(self):
        self.vBoxLayout = QVBoxLayout(self.view)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(25)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.addWidget(self.intro)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadSamples(self):
        pass

    def __connectSignalToSlot(self):
        pass