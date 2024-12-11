"""Основной модуль"""


import os
import re

from src.widget_settings import WidgetSetting
from src.analyze import get_system_info
from src.delete import app_paths
from src.apps import get_apps

from databases.db import *
from values.ConstValues import *

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QMainWindow, QWidget, QTableWidget,
                             QLineEdit, QPushButton, QFileDialog,
                             QTableWidgetItem, QHeaderView, QTextEdit)


class System(QWidget):
    """Виджет, содержащий информацию о системе"""
    def __init__(self) -> None:
        super().__init__()

        self.__setupWindow()

        # SETUP WIDGETS

        self.textEdit = QTextEdit(self)
        WidgetSetting(self.textEdit, TEXT_EDIT_WIDTH, TEXT_EDIT_HEIGHT, TEXT_EDIT_X, TEXT_EDIT_Y)

    def __setupWindow(self) -> None:
        """Установка параметров окна с характеристиками системы"""
        self.setWindowTitle(SYSTEM_TITLE)
        self.setWindowIcon(QIcon(SYSTEM_ICON))
        self.setGeometry(SYSTEM_X, SYSTEM_Y, SYSTEM_WIDTH, SYSTEM_HEIGHT)
        self.setMinimumSize(SYSTEM_MIN_WIDTH, SYSTEM_MIN_HEIGHT)
        self.setMaximumSize(SYSTEM_MAX_WIDTH, SYSTEM_MAX_HEIGHT)

    def update_info(self, text: str) -> None:
        """Обновление текста в виджете"""
        self.textEdit.setText(text)


class Main(QMainWindow):
    """Основной класс приложения"""
    def __init__(self, _system) -> None:
        super().__init__()

        self.__system = _system

        self.__setupWindow()

        # SETUP WIDGETS

        self.pathEdit = QLineEdit(self)
        WidgetSetting(self.pathEdit, PATH_WIDTH, PATH_HEIGHT, PATH_X, PATH_Y)

        self.manuallyButton = QPushButton("Выбрать вручную", self)
        WidgetSetting(self.manuallyButton, MANUALLY_WIDTH, MANUALLY_HEIGHT, MANUALLY_X, MANUALLY_Y)
        self.manuallyButton.clicked.connect(self.__select_path)

        self.deleteButton = QPushButton("Удалить", self)
        WidgetSetting(self.deleteButton, DELETE_WIDTH, DELETE_HEIGHT, DELETE_X, DELETE_Y)
        self.deleteButton.clicked.connect(self.__delete_app)

        self.analysisButton = QPushButton("Анализ системы", self)
        WidgetSetting(self.analysisButton, ANALYSIS_WIDTH, ANALYSIS_HEIGHT, ANALYSIS_X, ANALYSIS_Y)
        self.analysisButton.clicked.connect(self.__analysis_system)

        self.openAppButton = QPushButton("Перейти в проводник", self)
        WidgetSetting(self.openAppButton, OPEN_WIDTH, OPEN_HEIGHT, OPEN_X, OPEN_Y)
        self.openAppButton.clicked.connect(self.__open_app)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(TABLE_COUNT_COLUMNS)
        self.tableWidget.setHorizontalHeaderLabels(HORIZONTAL_HEADER_LABELS)

        self.tableWidget.clicked.connect(self.__cellClicked)

        # Автоподбор размера названий столбцов
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        WidgetSetting(self.tableWidget, TABLE_WIDTH, TABLE_HEIGHT, TABLE_X, TABLE_Y)

        self.__apps = get_apps()

        # Загрузка данных в БД (Установленные приложения)
        load_apps(self.__apps)

        self.__system_info = ""
        for k, v in get_system_info().items():
            if k != "Видеокарты":
                self.__system_info += f"{k}: {v}\n"
            else:
                self.__system_info += f"\n{k}:\n    "
                for i in v:
                    for k1, v1 in i.items():
                        self.__system_info += f"    {k1}: {v1}\n    "

        self.__show_apps()

    def __setupWindow(self) -> None:
        """Установка параметров основного окна приложения"""
        self.setWindowTitle(MAIN_TITLE)
        self.setWindowIcon(QIcon(MAIN_ICON))
        self.setGeometry(MAIN_X, MAIN_Y, MAIN_WIDTH, MAIN_HEIGHT)
        self.setMinimumSize(MAIN_MIN_WIDTH, MAIN_MIN_HEIGHT)
        self.setMaximumSize(MAIN_MAX_WIDTH, MAIN_MAX_HEIGHT)

    def __show_apps(self) -> None:
        """Отображение всех приложений в таблице"""
        self.tableWidget.setRowCount(len(self.__apps))

        for i in range(len(self.__apps)):
            _name = self.__apps[i]["_name"]
            _version = self.__apps[i]["_version"]
            _date = self.__apps[i]["_date"]
            _install_location = self.__apps[i]["_install_location"]
            _source = self.__apps[i]["_source"]
            _author = self.__apps[i]["_author"]
            _uninstall_location = self.__apps[i]["_uninstall_location"]

            app = (_name, _version, _date, _install_location, _source, _author, _uninstall_location)

            for j in range(len(app)):
                self.tableWidget.setItem(i, j, QTableWidgetItem(app[j]))

    def __select_path(self) -> None:
        """Выбор пути к приложению в проводнике"""
        file_path = QFileDialog.getExistingDirectory(self, 'Выбор папки')
        self.pathEdit.setText(file_path)

    def __delete_app(self) -> None:
        """Удаление приложения по указанному пути"""
        if self.pathEdit.text() == "":
            if self.tableWidget.currentItem() is None:
                return

            __full_app_name = self.tableWidget.currentItem().row()["_name"]
            app_name = self.__apps[self.tableWidget.currentItem().row()]["_name"].lower()

            app_name = app_name[:app_name.find(re.findall(r'\d+.*\d+.*\d+', app_name)[0]) - 1]
            paths = app_paths(app_name)
            for path in paths:
                if os.path.exists(path):
                    os.rmdir(path)

            delete_app(__full_app_name, paths)

        else:
            path = self.pathEdit.text()

            print(path)
            os.rmdir(path)

            app_name = path[path.rfind("/") + 1:].lower()
            delete_app(app_name, [path])

            self.pathEdit.setText("")

    def __open_app(self) -> None:
        """Открытие файлов приложения"""
        if self.pathEdit.text() == "":
            if self.tableWidget.currentItem() is None:
                path = "C:/"
            else:
                path = self.__apps[self.tableWidget.currentItem().row()]["_install_location"]
                if path == "":
                    path = "C:/"
        else:
            path = self.pathEdit.text()
            path = path[:path.rfind("/")]

        if not path:
            path = "C:/"

        os.startfile(path)

        self.pathEdit.setText("")

    def __analysis_system(self) -> None:
        """Анализ системы"""
        self.__system.show()
        self.__system.update_info(self.__system_info)

    def __cellClicked(self) -> None:
        """Выделение всей строки по нажатию на ячейку таблицы"""
        self.tableWidget.selectRow(self.tableWidget.currentRow())
