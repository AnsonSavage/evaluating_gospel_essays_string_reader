from reference_counter import ReferenceCounter
import os

reference_counter = ReferenceCounter('input/guard_seek_paradigm_dec_7_2022.md')

reference_counter.print_results()

# Output the results to a file called "output/guard_seek_paradigm_dec_7_2022_results.txt". Make the file if it doesn't exit
if not os.path.exists('output'):
    os.mkdir('output')

with open('output/guard_seek_paradigm_dec_7_2022_results.txt', 'w') as fileobj:
    fileobj.write(str(reference_counter))