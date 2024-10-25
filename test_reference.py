import unittest
from .reference import Reference

class TestReference(unittest.TestCase):
    def test_valid_reference(self):
        ref_str = '- “This is a valid quote.” (123)'
        reference = Reference(ref_str)
        self.assertEqual(reference.reference_number, "123")

    def test_valid_reference_with_additional_text(self):
        ref_str = '- “Another valid quote.” (456) Additional commentary.'
        reference = Reference(ref_str)
        self.assertEqual(reference.reference_number, "456")

    def test_invalid_reference_no_dash(self):
        ref_str = '“This is a quote without a dash.” (789)'
        with self.assertRaises(AssertionError) as context:
            Reference(ref_str)
        self.assertIn("Reference string must contain a reference tag", str(context.exception))

    def test_invalid_reference_no_parentheses(self):
        ref_str = '- “This quote lacks parentheses.” 101'
        with self.assertRaises(AssertionError) as context:
            Reference(ref_str)
        self.assertIn("Reference string must contain a reference tag", str(context.exception))

    def test_invalid_reference_non_digit(self):
        ref_str = '- “This quote has non-digit reference.” (ABC)'
        with self.assertRaises(AssertionError) as context:
            Reference(ref_str)
        self.assertIn("Reference string must contain a reference tag", str(context.exception))

    def test_reference_with_two_digits(self):
        ref_str = '- “Two-digit reference.” (12)'
        reference = Reference(ref_str)
        self.assertEqual(reference.reference_number, "12")

    def test_reference_with_more_digits(self):
        ref_str = '- “Four-digit reference.” (1234)'
        reference = Reference(ref_str)
        self.assertEqual(reference.reference_number, "1234")

    def test_reference_with_nested_parentheses(self):
        ref_str = '- “Nested (parentheses) inside quote.” (678) More content.'
        reference = Reference(ref_str)
        self.assertEqual(reference.reference_number, "678")

    def test_reference_with_spaces(self):
        ref_str = '- “Quote with space before reference.”   (901)   Extra text.'
        reference = Reference(ref_str)
        self.assertEqual(reference.reference_number, "901")

    def test_reference_with_no_space_after_dash(self):
        ref_str = '-“Quote with no space after dash.”(234)'
        reference = Reference(ref_str)
        self.assertEqual(reference.reference_number, "234")

if __name__ == '__main__':
    unittest.main()
