import unittest
from model.conversions import convert_to_metric, convert_to_imperial, format_converted_amount

#Tolu tests
class TestConversions(unittest.TestCase):

    def test_convert_to_metric_cup(self):
        result = convert_to_metric(1, "cup")
        self.assertEqual(result, (236.588, "mL"))

    def test_convert_to_imperial_kg(self):
        result = convert_to_imperial(1, "kg")
        self.assertEqual(result, (1 / 0.453592, "lb"))

    def test_format_converted_amount_metric(self):
        result = format_converted_amount(1, "cup", "metric")
        self.assertEqual(result, "236.59 mL")

    def test_format_converted_amount_imperial(self):
        result = format_converted_amount(1, "kg", "imperial")
        self.assertEqual(result, "2.2 lb")

    def test_bad_unit(self):
        result = format_converted_amount(1, "weirdunit", "metric")
        self.assertEqual(result, "Unit not supported")

    def test_bad_system(self):
        result = format_converted_amount(1, "cup", "random")
        self.assertEqual(result, "System not supported")


if __name__ == "__main__":
    unittest.main()