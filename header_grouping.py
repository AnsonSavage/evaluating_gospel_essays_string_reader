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

    def add_direct_subheader(self, header):
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
    
    
    def __str__(self):
        tab_prefix = "\t" * self.header_level
        result_string = tab_prefix + self.header_text + "(" + str(self.get_all_descendants_references_including_self(unique=True)) + ")\n"

        if self.get_num_direct_references(unique=True) > 0:
            result_string += tab_prefix + "Total number of unique references for this header: " + str(self.get_num_direct_references(unique=True)) + "\n"
            result_string += tab_prefix + "References: " + str(self.references) + "\n"

        for sub_header in self.sub_headers:
            result_string += str(sub_header)
        return result_string
    

class HeaderManager:
    def __init__(self):
        self.root_header = Header("") # This is the root header, which is the header that is the parent of all other headers and has a level of 0
        self.current_header = self.root_header
        self.most_recent_header_dict = {self.root_header.get_header_level(): self.root_header}
    
    def add_header(self, line_text):
        new_header = Header(line_text)
        
        if new_header.get_header_level() > self.current_header.get_header_level(): # If the header is a subheader of the current header
            self.current_header.add_direct_subheader(new_header)
        else:
            if new_header.get_header_level() - 1 in self.most_recent_header_dict: # This is the case when a header directly follows another header that is one level higher
                # Find the most recent header that is a direct parent of the new header
                most_recent_header = self.most_recent_header_dict[new_header.get_header_level() - 1]
                most_recent_header.add_direct_subheader(new_header)
                self.most_recent_header_dict[new_header.get_header_level()] = new_header
            else: # This is the case when, for example, there is a level three header that jumps back to a level one header
                self.most_recent_header_dict[new_header.get_header_level()] = new_header

        self.current_header = new_header
    
    def add_reference(self, reference):
        self.current_header.add_reference(reference)
    
    def __str__(self):
        return str(self.root_header)
    
    def get_total_references_from_header_group(self, unique = True):
        return self.root_header.get_num_direct_references(unique= unique)