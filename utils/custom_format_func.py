def custom_format(number, separator=' '):
    if number is None:
        return "N/A"  # Или любое другое значение по умолчанию
    return f"{number:,}".replace(",", separator)
