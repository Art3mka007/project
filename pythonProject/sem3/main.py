import re


def extract(text: str) -> list[str]:
    """Извлекает из текста и вносит в единый список result артикулы или SKU"""
    found = re.findall(
        r"(?:SKU:?|артикул)\s*([A-Za-z0-9-]+)", text, re.IGNORECASE
    )

    pattern = re.compile(r"^[A-Za-z0-9-]+$")
    result = []

    for item in found:
        if pattern.match(item) and len(item) >= 3:
            result.append(item)

    return result


def read(path: str) -> list[str]:
    """Считывает файл с обработкой ошибок и возвращает список SKU, сформированный в функции extract."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = file.read()

        return extract(data)

    except FileNotFoundError:
        print(f"Ошибка: файл '{path}' не найден.")
        return []
    except UnicodeDecodeError:
        print(f"Ошибка чтения: неверная кодировка файла '{path}'.")
        return []
    except Exception as error:
        print(f"Произошла ошибка при обработке файла: {error}")
        return []

if __name__ == "__main__":
    result = read("orders.txt")
    print(result)