"""Задача 5. Розбір вкладеного JSON.

Правила: student.md, розділ «Опис задач», задача 5.
Відкриті тести: pytest tests/test_variant_05.py
"""


import requests

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "pp-p05-student"
}


def nested_stats(base_url: str, resource: str, item_id: int, list_field: str, value_field: str) -> dict:
    """Розбирає вкладений список з JSON запису й рахує підсумок."""

    url = f"{base_url}/api/v1/{resource}/{item_id}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=5
    )

    if response.status_code == 404:
        raise ValueError(f"Запис {item_id} не знайдено")

    if response.status_code != 200:
        raise RuntimeError(f"Помилка API: {response.status_code}")

    data = response.json()

    items = data.get(list_field)

    if not isinstance(items, list):
        raise ValueError(f"Немає списку: {list_field}")

    values = []
    skipped = 0

    for item in items:
        if not isinstance(item, dict):
            skipped += 1
            continue

        value = item.get(value_field)

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            values.append(value)
        else:
            skipped += 1

    if len(values) == 0:
        return {
            "count": 0,
            "min": None,
            "max": None,
            "mean": None,
            "skipped": skipped
        }

    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": round(sum(values) / len(values), 2),
        "skipped": skipped
    }
