import re
from header_grouping import HeaderManager

class ReferenceCounter:
    def __init__(self, file_path, print_references=True, count_duplicates=False):
        self.file_name = file_path
        self.self.print_references = print_references
        self.self.count_duplicates = count_duplicates
        self.p = re.compile(r'\(\d\d\d\)') # regex to find all references in the format (###), or three digits in a row, surrounded by parentheses
        self.total_reference_count = None

    def get_count(self):

        total_reference_count = 0

        with open(self.file_name) as fileobj:
            current_line = ""
            header_manager = HeaderManager()
            for line in fileobj:
                if line.startswith("#"): # This indicates that this line is a header of some kind
                    header_manager.add_header(line)
                elif line.startswith("-"): # This indicates that this line is quote block
                    current_articles = self.p.findall(line)  # This will return a list of all references in the current line
                    for article in current_articles:
                        header_manager.add_reference(article)
                else: # In this case, we can ignore everything that's not a header or a quote block
                    pass

        self.total_reference_count = total_reference_count
        return total_reference_count

    def print_results(self):
        assert self.total_reference_count is not None, "You must call get_count() before calling print_results()"

        for header in self.headers_and_references:
            print(header)
            references_for_header = len(self.headers_and_references[header])
            print("\t Reference count: ", references_for_header)
            print("\t Percent of total references: ",  '{:.2%}'.format(references_for_header / self.total_reference_count))

            if self.print_references:
                for reference in self.headers_and_references[header]:
                    print("\t \t", reference)

            print("\n")
            print("\n")
