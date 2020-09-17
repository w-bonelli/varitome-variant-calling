import subprocess
import os
import gzip
import shutil
from docker_tools import check_container_status
from string import ascii_letters
from string import digits
from sys import exit


def get_vcfs(input_bam_file, output_vcf_path):
    """
    Usage: get_vcfs(input_bam_file, output_vcf_path)
    :param: input_bam_file - One BAM file to be parsed.
    :param: output_vcf_path - The location where the generated VCF file to be placed.
    :return: Number indicating whether get_vcfs was run successfully.
        0 - ran successfully
        10 - output path did not include a name
    """
    if not os.path.exists(output_vcf_path):
        open(output_vcf_path, 'w').close()
    if not isinstance(input_bam_file, str) or \
        input_bam_file == '' or \
        not input_bam_file.endswith(".bam") or \
        not os.path.isfile(input_bam_file) or \
        not os.access(input_bam_file, os.R_OK) or \
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
              ".bam. While the output file must be located in an existing file directory, and its name may not be "
              "empty and may only contain ASCII characters, numbers, ., -, and _. Moreover, the intended path musts be"
              "writable and must end with .vcf.")
        exit()
        return

    print("Obtaining the VCF file from %s" % input_bam_file[input_bam_file.rfind('/') + 1:])

    check_container_status(input_bam_file[:input_bam_file.rfind('/') + 1])

    subprocess.run('docker exec -ti bio_c sh -c "cd /bio/ && lumpyexpress -B %s -o %s -P"'
                   % (input_bam_file[input_bam_file.rfind('/') + 1:],
                      output_vcf_path[output_vcf_path.rfind('/') + 1:]), shell=True)

    shutil.move(input_bam_file[:input_bam_file.rfind('/') + 1] + output_vcf_path[output_vcf_path.rfind('/') + 1:],
                output_vcf_path)

    return 0
#
#get_vcfs("/home/nathantaitano/Desktop/pimpiSVs/new_bams/EA00676.bam", "/home/nathantaitano/Desktop/pimpiSVs/new_bams/EA00676.vcf") 
#get_vcfs("/home/nathantaitano/Desktop/pimpiSVs/new_bams/BGV008037.bam", "/home/nathantaitano/Desktop/pimpiSVs/new_bams/BGV008037.vcf")