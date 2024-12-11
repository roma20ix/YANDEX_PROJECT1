"""Удаление файла по указанному пути"""


import os


def app_paths(app_name):
    """Функция, которая возвращает все директории, где в названиях есть подстрока app_name"""
    paths = set()

    for root, directories, files in os.walk(r"C:\\"):
        if "windows" in root.lower():
            # В папках Windows чаще всего не лежит пользовательских файлов
            # И так как файлов Windows КРАЙНЕ много, можно их пропускать
            # Эту проверку можно убрать, но тогда программа будет проверять все директории
            # Что займёт очень много времени
            continue

        root1 = root.lower()
        root1 = root1[root1.rfind("\\") + 1:]
        if app_name in root1:
            paths.add(root)

    return paths
