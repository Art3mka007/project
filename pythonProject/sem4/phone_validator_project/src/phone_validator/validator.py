import re

# Регулярное выражение для проверки российских номеров (поддерживает +7, 8, скобки и дефисы)
_PHONE_RE = re.compile(
    r"^(\+7|8)?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$"
)


def is_valid_phone(phone: str) -> bool:
    """Проверяет, является ли строка корректным телефонным номером.

    Args:
        phone: строка для проверки.

    Returns:
        True, если телефон похож на корректный, иначе False.

    Examples:
        >>> is_valid_phone("+7 (999) 123-45-67")
        True
        >>> is_valid_phone("invalid-phone")
        False
    """
    if not isinstance(phone, str):
        return False

    cleaned_phone = phone.strip()
    if not cleaned_phone:
        return False

    return _PHONE_RE.match(cleaned_phone) is not None