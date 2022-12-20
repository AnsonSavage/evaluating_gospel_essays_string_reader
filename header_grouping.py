class Header:
    def __init__(self, line_text):
        # Get total number of consecutive pound signs in the header
        self.header_level = len(line_text) - len(line_text.lstrip("#")) # Note that this assumes that the pound signs only appear at the beginning of the line

        # Make sure that there are no pound signs in the header itself by creating a substring starting at the first non-pound sign
        header_without_leading_pound_signs = line_text[self.header_level:].strip()
        assert not "#" in header_without_leading_pound_signs, "Header contains pound signs: " + header_without_leading_pound_signs
        
        self.header_text = header_without_leading_pound_signs
        self.sub_headers = []
        self.references= []

    def add_reference(self, reference):
        self.references.append(reference)

    def get_header_level(self):
        return self.header_level

    def add_subheader(self, header):
        self.sub_headers.append(header)
    
    def get_all_descendants_references_including_self(self, unique = True):
        total_number_of_references = self.get_num_direct_references(unique = unique)

        for sub_header in self.sub_headers:
            total_number_of_references += sub_header.get_all_descendants_references_including_self(unique = unique)
        return total_number_of_references
    
    def get_num_direct_references(self, unique = True):
        if unique:
            return len(set(self.references))
        return len(self.references)
    
    def join_integers_with_delimiter(self, integers, delimiter) -> str:
        return delimiter.join([str(integer) for integer in integers])
    
    def surround_string_with_parenthesis(self, string):
        return "(" + string + ")"

    def get_decendent_references_count_string(self) -> str:
        return self.surround_string_with_parenthesis(self.join_integers_with_delimiter([self.get_all_descendants_references_including_self(unique=True), self.get_all_descendants_references_including_self(unique=False)], "/"))
    
    def get_header_specific_references_count_string(self) -> str:
        return self.surround_string_with_parenthesis(self.join_integers_with_delimiter([self.get_num_direct_references(unique=True), self.get_num_direct_references(unique=False)], "/"))
    
    def generate_header_text(self):
        tab_prefix = "\t" * self.header_level
        return tab_prefix + "* " + self.header_text + " " + self.get_decendent_references_count_string() +"\n"
        
    def get_header_for_table_entry(self):
        prefix = "*" * self.header_level
        return "\"" + prefix + " " + self.header_text.replace(",", ";") + "\""
    
    def __str__(self):
        indent_prefix = "\t" * (self.header_level + 1)

        result_string = self.generate_header_text()
        if self.get_num_direct_references(unique=True) > 0:
            result_string += indent_prefix + "- " + "References directly linked to this principle " + self.get_header_specific_references_count_string() + "\n"
            result_string += indent_prefix + "- " + "References: " + str(self.references) + "\n"

        for sub_header in self.sub_headers:
            result_string += str(sub_header)
        return result_string
    
    def generate_own_table_entry(self):
        return [self.get_header_for_table_entry(), self.get_decendent_references_count_string(), self.get_header_specific_references_count_string(), str(self.references)]
    
    def add_table_entries(self, header_manager):
        header_manager.add_table_entry(self.generate_own_table_entry())
        for sub_header in self.sub_headers:
            sub_header.add_table_entries(header_manager)
        
    

class HeaderManager:
    def __init__(self):
        self.root_header = Header("") # This is the root header, which is the header that is the parent of all other headers and has a level of 0
        self.current_header = self.root_header
        self.most_recent_header_dict = {self.root_header.get_header_level(): self.root_header}
        self.table_representation = None
    
    def add_header(self, line_text):
        new_header = Header(line_text)
        
        self.most_recent_header_dict[new_header.get_header_level()] = new_header
        if new_header.get_header_level() > self.current_header.get_header_level(): # If the header is a subheader of the current header
            self.current_header.add_subheader(new_header)
        else:
            next_smallest_header_level = max([key for key in self.most_recent_header_dict.keys() if key < new_header.get_header_level()])
            self.most_recent_header_dict[next_smallest_header_level].add_subheader(new_header)

        self.current_header = new_header
    
    def add_reference(self, reference):
        self.current_header.add_reference(reference)
    
    def __str__(self):
        return str(self.root_header)
    
    def get_total_references_from_header_group(self, unique = True):
        return self.root_header.get_num_direct_references(unique= unique)
    
    def add_table_entry(self, table_entry: list):
        self.table_representation.append(table_entry)

    def get_table_representation(self):
        assert self.table_representation is None, "Table representation has already been generated"
        self.table_representation = []
        self.root_header.add_table_entries(self)
        return self.table_representation