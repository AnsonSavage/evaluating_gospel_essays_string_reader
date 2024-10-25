import re

quote_regex = re.compile(r"^-\s*.*\((\d+)\)")


class Reference:
    def __init__(self, reference_string):
        assert quote_regex.match(reference_string), "Reference string must contain a reference tag"
        
        # Extract the digits from the reference string
        self.reference_number = quote_regex.match(reference_string).group(1) # Should be a string
    
    def __str__(self):
        return self.reference_number