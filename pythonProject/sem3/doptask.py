import re


def extract(text: str) -> tuple[list[str], list[str]]:
    """Разбирает лог и фильтрацией вытаскивает ошибки/предупреждения и строки с IP."""
    # Регулярка разбивает строку лога на 3 группы: время, уровень и сообщение
    pattern = re.compile(
        r"^\d{4}-\d{2}-\d{2}\s+(\d{2}:\d{2}:\d{2})\s+([A-Z]+)\s+(.+)$",
        re.MULTILINE,
    )

    # Регулярка для поиска IP-адресов
    ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

    errors_warnings = []
    ip_logs = []

    for line in text.strip().splitlines():
        match = pattern.match(line)
        if match:
            time, level, message = match.groups()
            formatted = f"{time} {level} {message}"

            # 1) Фильтр по уровню: ERROR или WARN / WARNING
            if level in ("ERROR", "WARN", "WARNING"):
                errors_warnings.append(formatted)

            # 2) Фильтр по наличию IP-адреса в строке
            if ip_pattern.search(line):
                ip_logs.append(formatted)

    return errors_warnings, ip_logs


def read(path: str) -> tuple[list[str], list[str]]:
    """Считывает файл с логами с обработкой ошибок."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = file.read()

        return extract(data)

    except FileNotFoundError:
        print(f"Ошибка: файл '{path}' не найден.")
        return [], []
    except UnicodeDecodeError:
        print(f"Ошибка чтения: неверная кодировка файла '{path}'.")
        return [], []
    except Exception as error:
        print(f"Произошла ошибка при обработке файла: {error}")
        return [], []


# Вывод результатов в столбец
if __name__ == "__main__":
    errors, ips = read("log.txt")

    print("1) Строки с ERROR или WARN:")
    for item in errors:
        print(item)

    print("\n2) Строки с IP-адресами:")
    for item in ips:
        print(item)