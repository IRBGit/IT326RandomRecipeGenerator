UNIT_CONVERSIONS = {
    "cup": ("mL", 236.588),
    "cups": ("mL", 236.588),
    "tbsp": ("mL", 14.787),
    "tablespoon": ("mL", 14.787),
    "tsp": ("mL", 4.929),
    "teaspoon": ("mL", 4.929),
    "oz": ("g", 28.3495),
    "lb": ("kg", 0.453592)
}


def convert_to_metric(amount, unit):
    # make unit lowercase
    unit = unit.lower()

    # check if unit exists
    if unit in UNIT_CONVERSIONS:
        metric_unit = UNIT_CONVERSIONS[unit][0]
        rate = UNIT_CONVERSIONS[unit][1]
        converted_amount = amount * rate
        return converted_amount, metric_unit
    else:
        return "Unit not supported"


def format_converted_amount(amount, unit):
    # get converted value
    result = convert_to_metric(amount, unit)

    # stop if unit is bad
    if result == "Unit not supported":
        return "Unit not supported"

    converted_amount = result[0]
    metric_unit = result[1]

    # round final answer
    converted_amount = round(converted_amount, 2)

    return str(converted_amount) + " " + metric_unit

print(format_converted_amount(1, "cup"))
print(format_converted_amount(2, "tbsp"))
print(format_converted_amount(1, "lb"))