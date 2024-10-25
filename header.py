import re
header_regex = re.compile(r'(#*)\s(.*)\{#.*\}')
class Node:
    def __init__(self, header):
        self.header = header
        self.level = 0
        self.sub_headers = []
        self.references = []
    
    def get_num_references(self, unique=False):
        return len(self.references) if not unique else len(set([str(reference) for reference in self.references])) # Note, I'm using the str essentially as the hash function here
    
    def get_total_references(self, unique=False):
        return self.get_num_references(unique=unique) + sum(sub_header.get_total_references(unique=unique) for sub_header in self.sub_headers)

class Header(Node):
    def __init__(self, header_string):
        super().__init__(header_string)
        assert header_string.startswith("#"), "Header string must start with a #"
        assert header_regex.match(header_string), "Header string must contain a header tag"
        self.level = len(header_string) - len(header_string.lstrip("#"))
        # Group 1 from the header_regex will be the header level, and group 2 will be the header text
        self.header_text = header_regex.match(header_string).group(2).strip()
    

def print_tree(node, indent=0):
    if node.header is not None:
        print("  " * indent + node.header)
        print("  " * indent + "References: " + str(node.get_num_references()), "(Unique: " + str(node.get_num_references(True)) + ")")
        print("  " * indent + "Total References Including Subheaders: " + str(node.get_total_references()), "(Unique: " + str(node.get_total_references(True)) + ")")
        print("  " * indent + "References enummerated:", [str(reference) for reference in node.references])
    for sub_header in node.sub_headers:
        print_tree(sub_header, indent + 1)
