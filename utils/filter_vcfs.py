import os
from string import ascii_letters
from string import digits
from sys import exit

def filter_vcfs(input_vcf, output_vcf_path, average_depth_dict):
    """
    function called to sift through all the structural variant calls from Lumpy and find those that are most likely
    to be true positives. The parts of the filtering process include:
        - Removing Chr00 and any affiliated breakends
        - Removing SVs with the sum of evidence greater than read_depth * 2 (read_depth * 3 if the SV is a duplication)
        - Removing SVs with the sum of evidence less than read_depth / 3
        - Removing Svs with PE evidence = 0 or SR evidence = 0
    Usage: filter_vcfs(, average_depth_dict)
    :param
         - the directory with a /vcfs/ folder containing vcfs
        average_depth_dict - a dictionary containing the average depths of the bam files for vcfs to be filtered
            Example: {"BGV007865m.bam" : 40.8642, "BGV007875.bam" : 7.64714, "BGV006906.bam" : 36.3488, "BGV008223.bam"
             : 11.5011, "BGV006457.bam" : 18.9472, "BGV006336.bam" : 7.03893}
    :return: Number indicating whether get_vcfs was run successfully.
        0 - ran successfully
        7 - could not file any vcf files
    """
    if not os.path.exists(output_vcf_path):
        open(output_vcf_path, 'w').close()

    if not isinstance(input_vcf, str) or \
        not input_vcf.endswith(".vcf") or \
        not os.path.isfile(input_vcf) or \
        not os.access(input_vcf, os.R_OK) or \
        not isinstance(output_vcf_path, str) or \
        not output_vcf_path.endswith(".vcf") or \
        output_vcf_path.rfind('/') == -1 or \
        not os.path.isdir(output_vcf_path[:output_vcf_path.rfind('/') + 1]) or \
        output_vcf_path[output_vcf_path.rfind('/') + 1:] == '' or \
        not all(c in ascii_letters + digits + '-' + '_' + '.' for c in \
        output_vcf_path[output_vcf_path.rfind('/') + 1:]) or \
        not os.access(output_vcf_path, os.W_OK):
        print("Invalid input or output path supplied. The input file itself must exist and be readable and end with"
              ".vcf. While the output file must be located in an existing file directory, and its name may not be "
              "empty and may only contain ASCII characters, numbers, ., -, and _. Moreover, the intended path must be "
              "writable and must end with .vcf.")
        exit()
        return
    elif not isinstance(average_depth_dict, dict) or \
        not average_depth_dict:
        print("depth_dict must be a nonempty dictionary.")
        exit()
        return


    read_depth = float(average_depth_dict[input_vcf.split('/')[-1].split('.')[0] + '.bam'])

    writing_filtered_vcf = open(output_vcf_path, 'w')
    reading_unfiltered_vcf = open(input_vcf, 'r')
    line = reading_unfiltered_vcf.readline()

    # Add header info
    while line.startswith("##"):
        writing_filtered_vcf.write(line)
        line = reading_unfiltered_vcf.readline()

    # Add Filter info to filtered vcf
    writing_filtered_vcf.write('##FILTER=<ID=PEmin, Description="Must have at least one piece of PE evidence">\n')
    writing_filtered_vcf.write('##FILTER=<ID=SRmin, Description="Must have at least one piece of SR evidence">\n')
    writing_filtered_vcf.write('##FILTER=<ID=SR<=PE, Description="Must have a SR evidence weight less than or'
                               'equal to the weight of PE evidence.">\n')
    writing_filtered_vcf.write(
        '##FILTER=<ID=SUmax%i, Description="The total SU evidence for all other SVs must be'
        ' less than or equal to %d, or 3 * (average read depth)">\n' % (int(read_depth * 3), int(read_depth * 3)))
    writing_filtered_vcf.write('##FILTER=<ID=SUmin%i, Description="The total SU evidence must be greater than or'
                               ' equal to %d, or (average read depth) / 2">\n' % (
                                   int(read_depth / 2), int(read_depth / 2)))

    # Add more header info
    while line.startswith('#'):
        writing_filtered_vcf.write(line)
        line = reading_unfiltered_vcf.readline()

    # Filter SVs
    print("Filtering SVs from " + input_vcf[input_vcf.rfind('/') + 1:])
    count = 0
    line = reading_unfiltered_vcf.readline() # get rid of \n
    list_of_clean_ids = []
    while line:
        sv_columns = line.split('\t')
        if not int(sv_columns[9].split(':')[2]) == 0 and \
            not int(sv_columns[9].split(':')[3]) == 0 and \
            read_depth * 3 >= int(sv_columns[9].split(':')[1]) >= read_depth / 2:
                writing_filtered_vcf.write(line)
                if sv_columns[4] != "<DEL>" and \
                        sv_columns[4] != "<DUP>" and \
                        sv_columns[4] != "<INV>" and \
                        sv_columns[4] != "<DUP:TANDEM>" and \
                        sv_columns[4] != "<INS>" and \
                        sv_columns[4] != "<CNVL>":
                    list_of_clean_ids.append(sv_columns[2][:sv_columns[2].rfind('_')])
        else:
            count += 1

        line = reading_unfiltered_vcf.readline()

    reading_unfiltered_vcf.close()
    writing_filtered_vcf.close()

    print("Filtered out %s SVs." % count)

    return 0
