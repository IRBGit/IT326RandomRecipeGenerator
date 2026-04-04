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
    "pounds": ("kg", 0.453592)
}

UNIT_TO_IMPERIAL = {
    "ml": ("cup", 1 / 236.588),
    "mL": ("cup", 1 / 236.588),
    "g": ("oz", 1 / 28.3495),
    "kg": ("lb", 1 / 0.453592)
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


#Update:  Started backend code for measurement conversion. 
# * Added unit support and helper functions to convert ingredient amounts into metric values.
# backend conversion file made
# metric conversions
# imperial conversions
# formatting helper
# ingredient helper
# more unit support

#To DO: work while viewing a recipe, so the missing part is still:

# connecting this to actual recipe data
# using real ingredient amount/unit values
# hooking it into recipe display
# testing it in the actual app flow

# test examples
# print(format_converted_amount(1, "cup", "metric"))
# print(format_converted_amount(2, "tbsp", "metric"))
# print(format_converted_amount(1, "kg", "imperial"))