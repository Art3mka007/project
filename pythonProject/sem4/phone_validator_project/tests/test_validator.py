import pytest

from phone_validator import is_valid_phone

def test_all_valid_fixture_phones(valid_phones):
    """Проверка, что все номера из фикстуры валидны."""
    for phone in valid_phones:
        assert is_valid_phone(phone) is True, f"Должен быть валидным: {phone!r}"

def test_all_invalid_fixture_phones(invalid_phones):
    """Проверка, что все номера из фикстуры невалидны."""
    for phone in invalid_phones:
        assert is_valid_phone(phone) is False, f"Должен быть невалидным: {phone!r}"


#дополнительный вариант тестирования с помощью параметризации
@pytest.mark.parametrize(
    "phone, expected",
    [
        ("+7 (999) 123-45-67", True),       # со скобками и дефисами
        ("8-999-123-45-67", True),          # с дефисами через 8
        ("8 999 123 45 67", True),          # с пробелами
        ("+7(999)1234567", True),           # без пробелов со скобками
        ("+7 (999) 123--4567", False),      # двойной дефис внутри номера
        ("+7 (999)  123-45-67", False),     # двойной пробел внутри блока
        ("7 (999) 123-45-67", False),       # начинается просто с 7 (без + и без 8)
        ("+9 (999) 123-45-67", False),      # неверный код страны (не +7 и не 8)
    ],
)
def test_phone_formatting_variations(phone, expected):
    """Проверка допустимых и недопустимых комбинаций разделителей и префиксов."""
    assert is_valid_phone(phone) is expected
