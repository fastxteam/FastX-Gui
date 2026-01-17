@echo off
SetLocal EnableDelayedExpansion
(set QMAKE=C:\qt5\qt5-build\qtbase\bin\qmake.exe)
(set PATH=C:\qt5\qt5-build\qtbase\bin;!PATH!)
if defined QT_PLUGIN_PATH (
    set QT_PLUGIN_PATH=C:\qt5\qt5-build\qtbase\plugins;!QT_PLUGIN_PATH!
) else (
    set QT_PLUGIN_PATH=C:\qt5\qt5-build\qtbase\plugins
)
C:\qt5\qt5-build\qttools\bin\lupdate.exe %*
EndLocal
