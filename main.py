# This file takes a cleaner approach to what we had done before.

"""
It simply counts the number of references directly below each header and the number of references below each of its subheaders.


It'll start by looking at each line.
    If the line contains {# any number of characters }, then it's a header.
        We figure out what level the header it is by counting the number of consecutive # characters at the beginning of the line.
    If the line starts with a '-' and contains a reference in the format (###), then it's a quote.
We'll have a function that extracts the header level and header text from a line. In fact, it'll probably be a class that takes in this string.

We'll also have a class that takes in a reference string and extracts the reference number from it as well as the text, why not?
"""
import re

header_regex = re.compile(r'(#*)\s(.*)\{#.*\}')
quote_regex = re.compile(r"^-\s*.*\((\d+)\)")

class Header:
    def __init__(self, header_string):
        assert header_string.startswith("#"), "Header string must start with a #"
        assert header_regex.match(header_string), "Header string must contain a header tag"
        self.header_level = len(header_string) - len(header_string.lstrip("#"))
        # Group 1 from the header_regex will be the header level, and group 2 will be the header text
        self.header_text = header_regex.match(header_string).group(2).strip()
        self.sub_headers = []
        self.references = []

class Reference:
    def __init__(self, reference_string):
        assert quote_regex.match(reference_string), "Reference string must contain a reference tag"
        
        # Extract the digits from the reference string
        self.reference_number = quote_regex.match(reference_string).group(1) # Should be a string