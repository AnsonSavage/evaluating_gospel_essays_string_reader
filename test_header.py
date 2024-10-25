# test_parser.py
import unittest
from .header import Header

class TestHeader(unittest.TestCase):
    def test_valid_header_level_1(self):
        header_str = "# Introduction {#introduction}"
        header = Header(header_str)
        self.assertEqual(header.level, 1)
        self.assertEqual(header.header_text, "Introduction")
        self.assertEqual(header.sub_headers, [])
        self.assertEqual(header.references, [])

    def test_valid_header_level_3(self):
        header_str = "### Detailed Analysis {#detailed-analysis}"
        header = Header(header_str)
        self.assertEqual(header.level, 3)
        self.assertEqual(header.header_text, "Detailed Analysis")
        self.assertEqual(header.sub_headers, [])
        self.assertEqual(header.references, [])

    def test_invalid_header_no_hash(self):
        header_str = "Introduction {#introduction}"
        with self.assertRaises(AssertionError) as context:
            Header(header_str)
        self.assertIn("Header string must start with a #", str(context.exception))

    def test_invalid_header_no_tag(self):
        header_str = "# Introduction"
        with self.assertRaises(AssertionError) as context:
            Header(header_str)
        self.assertIn("Header string must contain a header tag", str(context.exception))

    def test_invalid_header_empty_string(self):
        header_str = ""
        with self.assertRaises(AssertionError) as context:
            Header(header_str)
        self.assertIn("Header string must start with a #", str(context.exception))

    def test_header_with_multiple_spaces(self):
        header_str = "##    Overview    {#overview}"
        header = Header(header_str)
        self.assertEqual(header.level, 2)
        self.assertEqual(header.header_text, "Overview")
    
    def test_header_with_special_characters(self):
        header_str = "### Analysis & Findings {#analysis-findings}"
        header = Header(header_str)
        self.assertEqual(header.level, 3)
        self.assertEqual(header.header_text, "Analysis & Findings")

if __name__ == '__main__':
    unittest.main()
