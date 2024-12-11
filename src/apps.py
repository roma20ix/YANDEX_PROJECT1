"""
Получение всех установленных программ на компьютере
ОС: Windows 10
"""


import winapps


def get_apps() -> list[dict]:
    """Список всех установленных программ, установленных на компьютере"""
    apps = []
    for app in winapps.list_installed():
        _name = app.name
        _version = app.version
        _date = app.install_date
        _install_location = app.install_location
        _source = app.install_source
        _author = app.publisher
        _uninstall_location = app.uninstall_string

        if _date is None or _date in {"", " "}:
            _date = ""
        else:
            _date = f"{_date.day}.{_date.month}.{_date.year}"

        if _install_location is None or _install_location in {"", " "}:
            _install_location = ""
        else:
            _install_location = f"{_install_location.absolute()}"  # Получение пути объекта WindowsPath

        if _source is None or _source in {"", " "}:
            _source = ""
        else:
            _source = f"{_source.absolute()}"

        apps.append({
            "_name": _name,
            "_version": _version,
            "_date": _date,
            "_install_location": _install_location,
            "_source": _source,
            "_author": _author,
            "_uninstall_location": _uninstall_location
        })

    apps.sort(key = lambda x: x["_name"])
    return apps
