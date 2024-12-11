"""
Проект по курсу "Основы промышленного программирования | Д24".
Автор: Иванов Роман Иванович.
Название: Программа для управления установленными приложениями.
"""


import sys

from main import System, Main
from databases.db import create_table

from PyQt6.QtWidgets import QApplication


def run() -> None:
    create_table()

    app = QApplication(sys.argv)

    _system = System()
    _main = Main(_system)

    _main.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()
