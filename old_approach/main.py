import argparse
import os
import csv
from reference_counter import ReferenceCounter

# Set up argument parser
parser = argparse.ArgumentParser(description="Process reference counts and output results.")
parser.add_argument('input_file', type=str, help='Path to the input markdown file')
parser.add_argument('output_results_file', type=str, help='Path to the output results file')
parser.add_argument('output_csv_file', type=str, help='Path to the output CSV file')

args = parser.parse_args()

# Create a ReferenceCounter instance with the input file
reference_counter = ReferenceCounter(args.input_file)

# Print results to console
reference_counter.print_results()

# Ensure the output directory exists
output_dir = os.path.dirname(args.output_results_file)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Write results to the output file
with open(args.output_results_file, 'w') as fileobj:
    fileobj.write(str(reference_counter))

# Write the table representation to a CSV file
with open(args.output_csv_file, 'w', newline='') as fileobj:
    csv_writer = csv.writer(fileobj, delimiter=',')
    csv_writer.writerows(reference_counter.get_table_representation())
