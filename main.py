import argparse
import os
import csv
from stack import Stack
from header import Header, Node, header_regex, print_tree
from reference import Reference, quote_regex
# This file takes a cleaner approach to what we had done before.

"""
It simply counts the number of references directly below each header and the number of references below each of its subheaders.


It'll start by looking at each line.
    If the line contains {# any number of characters }, then it's a header.
        We figure out what level the header it is by counting the number of consecutive # characters at the beginning of the line.
    If the line starts with a '-' and contains a reference in the format (###), then it's a quote.
We'll have a function that extracts the header level and header text from a line. In fact, it'll probably be a class that takes in this string.

We'll also have a class that takes in a reference string and extracts the reference number from it as well as the text, why not?

So, we'll need to loop through each line in the file and keep track of the current header we're in. If we encounter a header, we'll update the current header to be this new header. If we encounter a reference, we'll add it to the current header's references list.
If the level of the new header being generated is greater than the current header, then it's a subheader of the current header. We'll add it to the current header's subheaders list.
If the level of the new header being generated is less than the current header, then it's a subheader of the current header's parent. We'll add it to the parent's subheaders list.
"""


def parse_markdown(markdown):
    root = Node(None)
    stack = Stack([root])
    for line in markdown.split("\n"):
        if header_regex.match(line):
            header = Header(line)
            while not stack.is_empty() and stack.peek().level >= header.level:
                stack.pop()
            parent = stack.peek()
            parent.sub_headers.append(header)
            stack.push(header)
        elif quote_regex.match(line):
            reference = Reference(line)
            stack.peek().references.append(reference)
        else:
            continue
    return root


# Set up argument parser
parser = argparse.ArgumentParser(description="Process reference counts and output results.")
parser.add_argument('input_file', type=str, help='Path to the input markdown file')
parser.add_argument('output_csv_file', type=str, help='Path to the output CSV file')

args = parser.parse_args()

# Read the input file
with open(args.input_file, 'r') as file:
    markdown = file.read()
    root = parse_markdown(markdown)

print_tree(root)


def export_to_csv(node, filename):
    """
    Traverses the Node tree and exports header information to a CSV file.

    Parameters:
    - node (Node): The root node of the tree.
    - filename (str): The name of the CSV file to create.
    """
    # Prepare the data list
    data = []

    def traverse(current_node, path):
        if current_node.header is not None:
            # Indicate hierarchy by indenting the header name
            indent = "  " * (current_node.level - 1)
            header_display = f"{indent}{'#' * current_node.level} {current_node.header_text}"
            
            # Gather reference counts
            references_direct = current_node.get_num_references()
            references_unique = current_node.get_num_references(True)
            references_total = current_node.get_total_references()
            references_total_unique = current_node.get_total_references(True)
            
            # Append the row to data
            data.append([
                header_display,
                references_direct,
                references_unique,
                references_total,
                references_total_unique
            ])
        
        # Traverse subheaders
        for sub_header in current_node.sub_headers:
            traverse(sub_header, path + [current_node.header_text] if current_node.header else path)

    # Start traversal from the root node
    traverse(node, [])

    # Define CSV headers
    csv_headers = [
        "Header Name",
        "Direct References",
        "Direct References (Not double counting quotes from the same talk)",
        "References (Including subheaders)",
        "References (Including subheaders, not double counting quotes from the same talk)"
    ]

    # Write data to CSV
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_headers)
            writer.writerows(data)
        print(f"Data successfully exported to '{filename}'.")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

export_to_csv(root, args.output_csv_file)