class Header:
    def __init__(self, line_text):
        # Get total number of consecutive pound signs in the header
        self.header_level = len(line_text) - len(line_text.lstrip("#")) # Note that this assumes that the pound signs only appear at the beginning of the line

        # Make sure that there are no pound signs in the header itself by creating a substring starting at the first non-pound sign
        header_without_leading_pound_signs = line_text[self.header_level:]
        assert not "#" in header_without_leading_pound_signs, "Header contains pound signs: " + header_without_leading_pound_signs
        
        self.header_text = header_without_leading_pound_signs
        self.sub_headers = []
        self.num_references = 0

    def increment_reference_count(self):
        self.num_references += 1

    def get_header_level(self):
        return self.header_level