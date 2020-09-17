import os
from string import ascii_letters
from string import digits
from sys import exit

def remove_chr00(input_vcf, output_vcf_path):
    """
    function called to sift through all the structural variant calls from Lumpy and find those that are most likely
    to be true positives. The parts of the filtering process include:
        - Removing Chr00 and any affiliated breakends
        - Removing SVs with the sum of evidence greater than read_depth * 2 (read_depth * 3 if the SV is a duplication)
        - Removing SVs with the sum of evidence less than read_depth / 3
        - Removing Svs with PE evidence = 0 or SR evidence = 0
    Usage: filter_vcfs(, average_depth_dict)
    :param: input_vcf - the vcf file that needs chromosome 00 SV calls removed.
    :param: output_vcf_path - what the filtered vcf file ought to be named and placed.
    :return: Number indicating whether get_vcfs was run successfully.
        0 - ran successfully
        7 - could not file any vcf files
    """
    if not os.path.exists(output_vcf_path):
        open(output_vcf_path, 'w').close()

    if not isinstance(input_vcf, str) or \
        input_vcf == '' or \
        not input_vcf.endswith(".vcf") or \
        not os.path.isfile(input_vcf) or \
        not os.access(input_vcf, os.R_OK) or \
        not isinstance(output_vcf_path, str) or \
        output_vcf_path == '' or \
        not output_vcf_path.endswith(".vcf") or \
        output_vcf_path.rfind('/') == -1 or \
        not os.path.isdir(output_vcf_path[:output_vcf_path.rfind('/') + 1]) or \
        output_vcf_path[output_vcf_path.rfind('/') + 1:] == '' or \
        not all(c in ascii_letters + digits + '-' + '_' + '.' for c in \
        output_vcf_path[output_vcf_path.rfind('/') + 1:]) or \
        not os.access(output_vcf_path, os.W_OK):
        print("Invalid Input or Output path supplied. The input file itself must exist and be readable and end with"
              ".vcf. While the output file must be located in an existing file directory, and its name may not be "
              "empty and may only contain ASCII characters, numbers, ., -, and _. Moreover, the intended path musts be"
              "writable and must end with .vcf.")
        exit()
        return

    chr_0_be_ids = []

    writing_filtered_vcf = open(output_vcf_path, 'w')
    reading_unfiltered_vcf = open(input_vcf, 'r')
    line = reading_unfiltered_vcf.readline()

    # Add header info
    while line.startswith("##"):
        writing_filtered_vcf.write(line)
        line = reading_unfiltered_vcf.readline()

    # Add Filter info to filtered vcf
    writing_filtered_vcf.write('##FILTER=<ID=CHR00, Description="Filters out Chr00 and all related breakends">\n')

    # Add more header info
    if line.startswith('#'):
        writing_filtered_vcf.write(line)
        line = reading_unfiltered_vcf.readline()

    # Filter SVs
    print("Filtering Chr00 from " + input_vcf[input_vcf.rfind('/') + 1:])
    count = 0
    while line:
        sv_columns = line.split('\t')
        if sv_columns[0].endswith("00"):  # Detects SVs on chromosome 00
            if sv_columns[4] != ("<DEL>" or "<DUP>" or "<INV>" or "<DUP>" or "<INS>" or "<CNV>"):  # If not a BND
                try:
                    index = chr_0_be_ids.index(sv_columns[2][:-1])
                    chr_0_be_ids.pop(index)
                except ValueError:
                    chr_0_be_ids.append(sv_columns[2][:-1])
            count += 1
        else:
            if not sv_columns[2][:-1] in chr_0_be_ids:
                writing_filtered_vcf.write(line)
            else:
                count += 1
        line = reading_unfiltered_vcf.readline()

    reading_unfiltered_vcf.close()
    writing_filtered_vcf.close()

    print("Filtered out %s SVs." % count)

    return 0