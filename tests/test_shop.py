import pytest
import sys
sys.path.append("D:/TeachMeSkills/Lesson19/src")
from shop import Shop

# Фикстура для инициализации объекта Shop перед каждым тестом
@pytest.fixture
def shop():
    return Shop()

# Добавление товара в корзину с положительным количеством
@pytest.mark.parametrize("item, quantity, expected", [
    ('vino', 3, {'vino': 3}),
    ('apple', 5, {'apple': 5}),
    ('apple', 3, {'apple': 3}),  # Ожидаем, что количество яблок не будет увеличиваться
])
def test_add_to_cart(shop, item, quantity, expected):
    """Тест добавления товара в корзину с разным количеством."""
    result = shop.add_to_cart(item, quantity)
    assert result == expected

# Поведение при попытке добавить товар с отрицательным или нулевым количеством
def test_add_to_cart_negative_quantity(shop):
    with pytest.raises(ValueError, match="Количество должно быть больше 0"):
        shop.add_to_cart('apple', -1)

    with pytest.raises(ValueError, match="Количество должно быть больше 0"):
        shop.add_to_cart('apple', 0)

# Расчёт общей стоимости корзины на основе цен
@pytest.mark.parametrize("cart, prices, expected_total", [
    ({'apple': 5}, {'apple': 9}, 45),  # 45
    ({'vino': 15}, {'vino': 3}, 45),  # 45
    ({'water': 0}, {'water': 0}, 0),  # 0
    ({'apple': 2, 'vino': 5}, {'apple': 9, 'vino': 3}, 33),  # 33
])
def test_calculate_total(shop, cart, prices, expected_total):
    shop.cart = cart
    result = shop.calculate_total(prices)
    assert result == expected_total

# Применение скидки на общую стоимость корзины
@pytest.mark.parametrize("total, discount, expected_total", [
    (100, 10, 90),   # 100 - 10% = 90
    (200, 20, 160),  # 200 - 20% = 160
    (100, 0, 100),   # 100 - 0% = 100
    (150, 100, 0),   # 150 - 100% = 0
])
def test_apply_discount(shop, total, discount, expected_total):
    result = shop.apply_discount(total, discount)
    assert result == expected_total

# Поведение при недопустимом значении скидки
def test_apply_discount_invalid(shop):
    with pytest.raises(ValueError, match="Скидка должна быть от 0 до 100"):
        shop.apply_discount(100, -1)

    with pytest.raises(ValueError, match="Скидка должна быть от 0 до 100"):
        shop.apply_discount(100, 101)