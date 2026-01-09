# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl, QSize, QEventLoop, QTimer, QTranslator
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QSplashScreen

from qfluentwidgets import isDarkTheme, FluentTranslator

from app.view.main_window import MainWindow
from app.common.config import cfg, Language


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # internationalization
    locale = cfg.get(cfg.language).value
    fluentTranslator = FluentTranslator(locale)
    galleryTranslator = QTranslator()
    galleryTranslator.load(locale, "gallery", ".", ":/gallery/i18n")

    app.installTranslator(fluentTranslator)
    app.installTranslator(galleryTranslator)

    w = MainWindow()
    w.show()
    app.exec_()
