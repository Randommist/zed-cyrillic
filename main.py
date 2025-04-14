import json5
import json


# Словарь для замены латинских символов на кириллические
cyrillic_map = {
    "`": "cyrillic_io",
    "q": "cyrillic_shorti",
    "w": "cyrillic_tse",
    "e": "cyrillic_u",
    "r": "cyrillic_ka",
    "t": "cyrillic_ie",
    "y": "cyrillic_en",
    "u": "cyrillic_ghe",
    "i": "cyrillic_sha",
    "o": "cyrillic_shcha",
    "p": "cyrillic_ze",
    "[": "cyrillic_ha",
    "]": "cyrillic_hardsign",
    "a": "cyrillic_ef",
    "s": "cyrillic_yeru",
    "d": "cyrillic_ve",
    "f": "cyrillic_a",
    "g": "cyrillic_pe",
    "h": "cyrillic_er",
    "j": "cyrillic_o",
    "k": "cyrillic_el",
    "l": "cyrillic_de",
    ";": "cyrillic_zhe",
    "'": "cyrillic_e",
    "z": "cyrillic_ya",
    "x": "cyrillic_che",
    "c": "cyrillic_es",
    "v": "cyrillic_em",
    "b": "cyrillic_i",
    "n": "cyrillic_te",
    "m": "cyrillic_softsign",
    ",": "cyrillic_be",
    ".": "cyrillic_yu",
}


def needs_localization(keystroke):
    """Проверяет, нужно ли переводить последнюю часть комбинации"""
    groups = keystroke.split()
    if not groups:
        return False
    last_group = groups[-1]
    parts = last_group.split("-")
    return parts[-1].lower() in cyrillic_map


def localize_keystroke(keystroke):
    """Переводит только последнюю часть в последней группе"""
    groups = keystroke.split()
    if not groups:
        return None

    # Обрабатываем только последнюю группу
    last_group = groups[-1]
    parts = last_group.split("-")
    last_part = parts[-1].lower()

    if last_part not in cyrillic_map:
        return None

    # Сохраняем регистр оригинальной части
    original_last_part = parts[-1]
    localized_part = cyrillic_map[last_part]
    if original_last_part.isupper():
        localized_part = localized_part.upper()

    # Заменяем последнюю часть
    parts[-1] = localized_part
    new_last_group = "-".join(parts)

    # Собираем все группы
    new_groups = groups[:-1] + [new_last_group]
    return " ".join(new_groups)


def process_keymap(data):
    """Обрабатывает keymap, сохраняя только локализованные комбинации"""
    for item in data:
        if "bindings" not in item:
            continue

        new_bindings = {}
        for keystroke, action in item["bindings"].items():
            if not needs_localization(keystroke):
                continue  # Пропускаем комбинации без перевода

            localized_keystroke = localize_keystroke(keystroke)
            if localized_keystroke:
                new_bindings[localized_keystroke] = action

        item["bindings"] = new_bindings

    return data


def main():
    try:
        with open("keymap.json", "r", encoding="utf-8") as f:
            data = json5.load(f)

        processed_data = process_keymap(data)

        with open("localized_keymap.json", "w", encoding="utf-8") as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f"Ошибка: {str(e)}")


if __name__ == "__main__":
    main()
