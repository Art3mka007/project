def check_cow_temperature(sensor_current_ma: float) -> str:
    """
    Анализирует сигнал от температурного датчика ДТК75(4-20) и возвращает
    текстовую диагностику состояния датчика и здоровья коровы.

    Аргументы:
        sensor_current_ma (float, int): Текущее значение выходного сигнала датчика в мА.

    Возвращает:
        str: Строка с результатами диагностики.

    Исключения:
        TypeError: Если на вход передано не число (int или float).
    """
    # Проверка типа входных данных
    if not isinstance(sensor_current_ma, (int, float)):
        raise TypeError(
            f"Ожидалось число (int или float) для значения датчика, "
            f"получен тип {type(sensor_current_ma).__name__} со значением {sensor_current_ma!r}."
        )

    # Параметры датчика ДТК75(4-20)
    pv_min = 0.0  # минимальное значение диапазона температур
    pv_max = 75.0  # максимальное значение диапазона температур
    i_min = 4.0  # минимальный нормальный сигнал (мА)
    i_max = 20.0  # максимальный нормальный сигнал (мА)

    # 1. Диагностика состояния датчика
    if sensor_current_ma < 0:
        return f"Получен некорректный сигнал {sensor_current_ma}мА (значение не может быть отрицательным)."

    if sensor_current_ma == 0.0:
        return f"Получен сигнал датчика {sensor_current_ma}мА, датчик отключен."

    if (0.0 < sensor_current_ma < 3.9) or (sensor_current_ma > 20.1):
        return f"Получен сигнал датчика {sensor_current_ma}мА, датчик неисправен."

    sensor_status = "датчик исправен"

    # 2. Расчет температуры
    # Формула: PV = (I - 4) * (PVmax - PVmin) / (20 - 4) + PVmin
    temperature = (sensor_current_ma - i_min) * (pv_max - pv_min) / (i_max - i_min) + pv_min

    # 3. Диагностика состояния коровы
    if temperature < 35.0:
        cow_status = "требуется внимание (датчик свалился или корова плохо себя чувствует)"
    elif 35.0 <= temperature < 37.5:
        cow_status = "корова замерзла, требуется обогрев"
    elif 37.5 <= temperature <= 39.0:
        cow_status = "с коровой все ок"
    elif 39.0 < temperature <= 39.5:
        cow_status = "корова перегрелась, требуется охлаждение"
    else:  # temperature > 39.5
        cow_status = "срочно вызывайте ветеринара, коровка заболела"

    return (f"Получен сигнал датчика {sensor_current_ma}мА, {sensor_status}, "
            f"температура {temperature:.1f} градусов, {cow_status}")

# Примеры использования:

# 1. Корректный вызов (float)
# print(check_cow_temperature(12.11))
# Вывод: Получен сигнал датчика 12.11мА, датчик исправен, температура 38.0 градусов, с коровой все ок

# 2. Корректный вызов (int)
# print(check_cow_temperature(0))
# Вывод: Получен сигнал датчика 0мА, датчик отключен.

# 3. Вызов с ошибкой типа (раскомментируйте, чтобы проверить)
# print(check_cow_temperature("12.11"))
# Выбросит исключение: TypeError: Ожидалось число (int или float) для значения датчика, получен тип str со значением '12.11'.