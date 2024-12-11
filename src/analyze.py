"""Получение данных о системе"""

import platform
import psutil
import GPUtil


def get_system_info():
    # Информация о системе
    _system_info = {
        "ОС": platform.system(),
        "Версия ОС": platform.version(),
        "Имя компьютера": platform.node(),
        "Архитектура": platform.architecture(),
        "Процессор": platform.processor(),
        "Количество ядер": psutil.cpu_count(logical=False),
        "Количество логических процессоров": psutil.cpu_count(logical=True),
        "Общая память (ГБ)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "Используемая память (ГБ)": round(psutil.virtual_memory().used / (1024 ** 3), 2),
        "Свободная память (ГБ)": round(psutil.virtual_memory().available / (1024 ** 3), 2),
    }

    # Информация о видеокартах
    _gpu_info = []

    for gpu in GPUtil.getGPUs():
        _gpu_info.append({
            "Имя": gpu.name,
            "Общая память (МБ)": gpu.memoryTotal,
            "Используемая память (МБ)": gpu.memoryUsed,
            "Версия драйвера": gpu.driver,
            "Температура (°C)": gpu.temperature,
            "Загрузка (%)": gpu.load * 100.0,
        })

    _system_info["Видеокарты"] = _gpu_info

    return _system_info
