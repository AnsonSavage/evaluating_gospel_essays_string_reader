import re

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
            current_header = None
            for line in fileobj:
                if line.startswith("#"): # This indicates that this line is a header of some kind
                    current_line = line
                    self.headers_and_references[line] = []

                else:
                    current_articles = self.p.findall(line)  # This will return a list of all references in the current line
                    if len(current_articles) > 0:
                        for article in current_articles:
                            if self.count_duplicates: # If we want to count duplicates, we can just append the article to the list
                                total_reference_count += 1
                                self.headers_and_references[current_line].append(article)
                            else: # Otherwise, we need to check if the article is already in the list
                                if not article in self.headers_and_references[current_line]:
                                    self.headers_and_references[current_line].append(article)
                                    total_reference_count += 1

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
