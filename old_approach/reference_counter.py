import re
from header_grouping import HeaderManager

class ReferenceCounter:
    def __init__(self, file_path):
        self.file_name = file_path
        self.p = re.compile(r'\(\d\d\d\)') # regex to find all references in the format (###), or three digits in a row, surrounded by parentheses
        self.total_reference_count = None
        self.header_manager = HeaderManager()
        self._initialize_header_manager()

    def _initialize_header_manager(self):
        with open(self.file_name) as fileobj:
            for line in fileobj:
                if line.startswith("#"): # This indicates that this line is a header of some kind
                    self.header_manager.add_header(line)
                elif line.startswith("-"): # This indicates that this line is quote block
                    current_articles = self.p.findall(line)  # This will return a list of all references in the current line
                    assert len(current_articles) == 1, "There should only be one reference per line"
                    self.header_manager.add_reference(current_articles[0])
                else: # In this case, we can ignore everything that's not a header or a quote block
                    pass

    def print_results(self):
        print(str(self))
    
    def get_table_representation(self):
        table_headers = ["Name of Principle", "Number of References Specific to Principle (Unique/All)", "Number of References for Principle and Subprinciples (Unique/All)", "Enumerated References for Principle"]
        table_body = self.header_manager.get_table_representation()
        
        # combine table headers and body
        table = [table_headers] + table_body
        return table
        
    
    def get_total_number_of_references(self):
        return self.total_reference_count
    
    def __str__(self):
        return self.header_manager.__str__()
    