import os
import get_accession
import merge_bam_list
from shutil import copyfile


def merge_bams(input_directory, output_directory=None, accession_file=None, v=False, k=False):
    """
    Merges bam files of the same accession together. Accessions of bam
    files are found using the get_accessions.get_accessions function,
    which parses the header of the bam file to find the accession. The
    accession is then stored in a file named accession_list.txt. After the
    accession of all bam files are known, those of the same accession are
    matched and passed to merge_bam_set, which uses samtools merge to
    merge the files.

    Usage:
    python merge_bams.py -i /directory/containing/bams -o /optional/output/directory

    Parameters:
        Required:
            -i: directory containing bam files to be merged
        Optional:
            -o: directory where merged bam files will be output
                Default: same directory as input bam files
            -a: a text file containing the accessions of bam files to be merged.
                The format looks like <accession_name>:<bam_file_name>
                For example: BGV005921:BGV005921-1.bam
                Default: this file can be automatically generated if not provided
            -k: keep an automatically generated text file that maps accessions to bam files
            -v: verbose mode
            -h: help (display this message)
    """

    if v: print("Finding bam files in %s" % input_directory)
    file_list = os.listdir(input_directory)
    bam_list = []
    for file in file_list:
        if file.endswith(".bam"):
            file = input_directory + '/' + file
            bam_list.append(file)

    accession_dict = {}

    if accession_file is not None and not isinstance(accession_file, dict) and accession_file.endswith(".txt"):
        if v: print("Parsing accession file at %s" % accession_file)
        try:
            open_accession_file = open(accession_file, 'r')
        except:
            print("Invalid accession text file provided")
            return 4
        line = open_accession_file.readline()
        while line:
            bam_name, accession= line.split(':')
            if accession.endswith('\n'):
                accession = accession[:-1]
            for bam_file in bam_list:
                bam_file_name = bam_file.split('/')[-1]
                if bam_file_name == bam_name:
                    accession_dict[accession] = accession_dict.get(accession, [])
                    accession_dict[accession].append(bam_file)
                    bam_list.remove(bam_file)
            line = open_accession_file.readline()

    if v: print("Checking the accessions of unparsed bam files")
    for bam_file in bam_list:
        bam_file_name = bam_file.split('/')[-1]
        accession = get_accession.get_accession(bam_file, accession_file=accession_file, q=k, v=v)
        accession_dict[accession] = accession_dict.get(accession, [])
        accession_dict[accession].append(bam_file)

    if v: print("Iterating through accessions to be merged")
    merged_accessions = []
    for accession, bam_list in accession_dict.items():
        if len(bam_list) > 1:
            if v:
                print("Merging bam files of %s:" % accession)
                for bam in bam_list:
                    print(bam)
            merge_bam_list.merge_bam_list(bam_list, output_directory=output_directory, accession=accession, v=v)
            merged_accessions.append(accession)
        else:
            if v:
                print("Cannot merge bam files of %s:" % accession)
                for bam in bam_list:
                    print(bam)
            copyfile(bam_list[0], output_directory + bam_list[0][bam_list[0].rfind('/'):])

    print("Merged bam files for %i accessions:" % len(merged_accessions))
    for accession in merged_accessions:
        print(accession)
    return 0