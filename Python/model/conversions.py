#------------------------------------------------------------
UNIT_TO_METRIC = {
    "cup": ("mL", 236.588),
    "cups": ("mL", 236.588),
    "tbsp": ("mL", 14.787),
    "tablespoon": ("mL", 14.787),
    "tablespoons": ("mL", 14.787),
    "tsp": ("mL", 4.929),
    "teaspoon": ("mL", 4.929),
    "teaspoons": ("mL", 4.929),
    "oz": ("g", 28.3495),
    "ounce": ("g", 28.3495),
    "ounces": ("g", 28.3495),
    "lb": ("kg", 0.453592),
    "pound": ("kg", 0.453592),
    "pounds": ("kg", 0.453592),
    "quart": ("L", 0.946353),
    "quarts": ("L", 0.946353)
}

UNIT_TO_IMPERIAL = {
    "ml": ("cup", 1 / 236.588),
    "mL": ("cup", 1 / 236.588),
    "g": ("oz", 1 / 28.3495),
    "kg": ("lb", 1 / 0.453592),
    "l": ("quart", 1 / 0.946353),
    "L": ("quart", 1 / 0.946353)
}


def convert_to_metric(amount, unit):
    # make unit lowercase
    unit = unit.lower()

    # check if unit exists
    if unit in UNIT_TO_METRIC:
        metric_unit = UNIT_TO_METRIC[unit][0]
        rate = UNIT_TO_METRIC[unit][1]
        converted_amount = amount * rate
        return converted_amount, metric_unit

    return "Unit not supported"


def convert_to_imperial(amount, unit):
    # check if unit exists
    if unit in UNIT_TO_IMPERIAL:
        imperial_unit = UNIT_TO_IMPERIAL[unit][0]
        rate = UNIT_TO_IMPERIAL[unit][1]
        converted_amount = amount * rate
        return converted_amount, imperial_unit

    return "Unit not supported"


def format_converted_amount(amount, unit, system):
    # convert to metric
    if system == "metric":
        result = convert_to_metric(amount, unit)

    # convert to imperial
    elif system == "imperial":
        result = convert_to_imperial(amount, unit)

    # bad system name
    else:
        return "System not supported"

    # stop if unit is bad
    if result == "Unit not supported":
        return "Unit not supported"

    converted_amount = result[0]
    converted_unit = result[1]

    # round final answer
    converted_amount = round(converted_amount, 2)

    return str(converted_amount) + " " + converted_unit


def convert_ingredient(amount, unit, name, system):
    # convert one ingredient line
    converted = format_converted_amount(amount, unit, system)

    # stop if unit is bad
    if converted == "Unit not supported":
        return "Unit not supported for " + name

    # stop if system is bad
    if converted == "System not supported":
        return "System not supported"

    return converted + " " + name


def split_quantity_text(quantity_text):
    # break text into parts
    parts = quantity_text.split()

    # no text given
    if len(parts) == 0:
        return None, None

    # try to read first part as number
    try:
        amount = float(parts[0])
    except ValueError:
        return None, None

    # only a number, no unit
    if len(parts) == 1:
        return amount, ""

    # save the unit part
    unit = " ".join(parts[1:])

    return amount, unit


def convert_quantity_text(quantity_text, system):
    # split amount and unit
    amount, unit = split_quantity_text(quantity_text)

    # bad quantity text
    if amount is None:
        return quantity_text

    # no unit to convert
    if unit == "":
        return quantity_text

    # convert the quantity
    converted = format_converted_amount(amount, unit, system)

    # keep old value if bad unit
    if converted == "Unit not supported":
        return quantity_text

    # keep old value if bad system
    if converted == "System not supported":
        return quantity_text

    return converted


def convert_recipe_ingredient(name, quantity_text, system):
    # convert full ingredient line
    converted_quantity = convert_quantity_text(quantity_text, system)

    return converted_quantity + " " + name


# test examples
# print(convert_quantity_text("1 quart", "metric"))
# print(convert_quantity_text("1.5 cups", "metric"))
# print(convert_quantity_text("0.5 teaspoon", "metric"))
# print(convert_quantity_text("2", "metric"))
# print(convert_recipe_ingredient("Milk", "1.5 cups", "metric"))
