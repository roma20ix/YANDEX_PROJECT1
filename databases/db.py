"""Модуль для работы с БД"""


import os
import datetime
import sqlite3 as sq


def create_table() -> None:
    """Создание БД"""

    # Проверка на то, что БД уже существует
    if os.path.exists("databases\\apps.db"):
        return

    con = sq.connect("databases\\apps.db")
    cur = con.cursor()

    # Таблица с установленными приложениями
    cur.execute("""CREATE TABLE 'applications' (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        _name TEXT,
        _version TEXT,
        _date TEXT,
        _install_location TEXT,
        _source TEXT,
        _author TEXT,
        _uninstall_location TEXT
    )""")

    # Таблица с удалёнными приложениями
    cur.execute("""CREATE TABLE 'deleted' (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        _name TEXT,
        _path TEXT,
        _date TEXT
    )""")

    con.close()


def load_apps(apps: list[dict]) -> None:
    """Обновление данных в БД (Установленные приложения)"""

    _apps = ""
    for i in range(len(apps)):
        _apps += f"{tuple('' if i is None else i for i in list(apps[i].values()))}"
        if i != len(apps) - 1:
            _apps += ",\n"

    con = sq.connect("databases\\apps.db")
    cur = con.cursor()

    # Загрузка данных в БД (Установленные приложения)
    cur.execute(f"""INSERT INTO applications 
    (_name, _version, _date, _install_location, _source, _author, _uninstall_location)
     VALUES {_apps}""")

    con.commit()

    con.close()


def delete_app(app_name: str, paths: list[str]) -> None:
    """Обновление данных в БД (Удалённые приложения)"""
    con = sq.connect("databases\\apps.db")
    cur = con.cursor()

    name_cols = tuple(cur.execute("SELECT _name FROM applications"))
    if tuple(app_name) in name_cols:
        cur.execute(f"""DELETE FROM applications WHERE _name = {app_name}""")

    q = ""
    for i in range(len(paths)):
        _now = datetime.datetime.now()
        _day = _now.day
        _month = _now.month
        _year = _now.year
        _second = _now.second
        _minute = _now.minute
        _hour = _now.hour

        q += f"{(app_name, paths[i], f'{_year}:{_month}:{_day}:{_hour}:{_minute}:{_second}')}"
        if i != len(paths) - 1:
            q += ",\n"

    cur.execute(f"""INSERT INTO deleted (_name, _path, _date) VALUES {q}""")

    con.commit()

    con.close()
