headers_and_references = {}
import re
p = re.compile(r'\(\d\d\d\)')

print_references = True
count_duplicates = False
file_name = "Benefits.txt"

total_reference_count = 0

with open(file_name) as fileobj:
    current_line = ""
    for line in fileobj:
        if line.startswith("##"):
            current_line = line
            headers_and_references[line] = []
        else:
            current_articles = p.findall(line)
            if len(current_articles) > 0:
                for article in current_articles:
                    if count_duplicates:
                        total_reference_count += 1
                        headers_and_references[current_line].append(article)
                    else:
                        if not article in headers_and_references[current_line]:
                            headers_and_references[current_line].append(article)
                            total_reference_count += 1
                        else:
                            pass


for header in headers_and_references:
    print(header)
    references_for_header = len(headers_and_references[header])
    print("\t Reference count: ", references_for_header)
    print("\t Percent of total references: ",  '{:.2%}'.format(references_for_header / total_reference_count))

    if print_references:
        for reference in headers_and_references[header]:
            print("\t \t", reference)

    print("\n")
    print("\n")
