"""
Модуль для установки параметров виджету
"""


from PyQt6.QtWidgets import (QTableWidget, QPushButton,
                             QLineEdit)


__types = [
    QPushButton,
    QLineEdit,
    QTableWidget
]

def WidgetSetting(obj: __types,
                  width: int,
                  height: int,
                  x: int,
                  y: int) -> None:
    """Функция для установки параметров виджетам"""
    obj.resize(width, height)
    obj.move(x, y)
