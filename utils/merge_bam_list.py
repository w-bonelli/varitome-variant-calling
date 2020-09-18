import os, sys, getopt
import subprocess
import docker_tools

usage = """
Merges bam files found in the input list.

First, fixes headers on bam files by using picard AddOrReplaceReadGroups (To be
merged, the header of all bam files must be EXACTLY the same). Original bam
files are left untouched and the fixed header bam files are deleted after they
are merged. After the headers are fixed, samtools merge is called on these bam
files. The merged bam file is output to the specified output directory.

To save time, if all bam files already have the same header, rename them to end
in "_fixed_header.bam".

Usage:
python merge_bam_list.py -i "path_to_first_bam, path_to_second_bam" -o /directory/for/merged/bam/

Parameters:
    Required:
        -i: list of paths to bam files to be merged
            IMPORTANT: these bam files MUST be in the same directory
    Optional:
        -o: output directory for the merged bam file
            Default: same folder as input files
        -a: accession of the bam files to be merged. The name of the 
            output file will be '<accession>m.bam'
            Default: the name of the first bam file
        -k: keep fixed header bam files
        -v: verbose mode
        -h: help
"""

def merge_bam_list(bam_list, output_directory=None, accession=None, v=False, k=False):
    mount_directory = os.path.dirname(bam_list[0])
    docker_tools.check_container_status(mount_directory)
    mount_directory += '/'

    if v: print("Fixing bam headers")
    fixed_header_bam_list = []
    for bam_file in bam_list:
        bam_name = bam_file.split('/')[-1]
        if bam_file.endswith("_fixed_header.bam"):
            fixed_header_bam_list.append("/bio/" + bam_name)
            continue
        else:
            fixed_header_bam = fix_header("/bio/" + bam_name, accession=accession)
            fixed_header_bam_list.append(fixed_header_bam)

    if v: print("Merging bams")
    bam_file_string = ' '.join(fixed_header_bam_list)
    if accession is None:
        accession = bam_file_list[0].split('/')[-1][0:-17]      #Gets rid of "_fixed_header.bam"
    merged_file = "/bio/" + str(accession) + "m.bam"

    subprocess.call('docker exec -it bio_c sh -c "samtools merge -c %s %s"' \
                    % (merged_file, bam_file_string), shell=True)

    if not k:
        if v: print("Deleting fixed header bam files")
        for file in fixed_header_bam_list:
            fixed_header_file = mount_directory + file[5:]
            if fixed_header_file not in bam_list:
                os.remove(fixed_header_file)

    if output_directory is not None:
        merged_bam_base_name = merged_file[4:]
        output_location = output_directory + merged_bam_base_name
        os.rename(mount_directory + merged_bam_base_name, output_location)
    return


def fix_header(bam_file, accession=None):
    output_file = bam_file[0:-4] + "_fixed_header.bam"
    if accession is None:
        accession = bam_file.split('/')[-1][0:-4]
    
    subprocess.call('docker exec -it bio_c sh -c "java -jar /usr/local/bin/picard.jar AddOrReplaceReadGroups \
                    I=%s \
                    O=%s \
                    RGID=%s \
                    RGLB=%s \
                    RGPL=illumina \
                    RGPU=unit1 \
                    RGSM=%s"' \
                    % (bam_file, output_file, accession, accession, accession), shell=True)

    return output_file


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'i:o:kvh')
    except getopt.GetoptError:
        print(usage + "\nGetOptError\n")
        return
    needed = ['-i']

    #Set default values for arguments
    bam_file_list = None
    output_directory = None
    verbose = False
    keep_fixed_header_files = False

    #Assign arguments
    for opt, arg in opts:
        if opt == '-h':
            print(usage); return
        elif opt == '-v':
            verbose = True
        elif opt == '-k':
            keep_fixed_header_files = True
        elif opt == '-i':
            bam_file_list = arg
        elif opt == '-s':
            output_directory = arg

    for opt, arg in opts:
        if opt in needed:
            needed.remove(opt)
    if needed:
        print(usage)
        for missing in needed:
            print("Error: " + {
                    '-i': "list of input bam files required",
                    }[missing])
        print('')
        return

    merge_bam_list(bam_file_list, output_directory=output_directory, v=verbose, k=keep_fixed_header_files)

    return

#merge_bam_list(['bam1', 'bam2'], output_directory='/Users/awilliams21/Desktop', v=True)

if __name__ == "__main__":
    main(sys.argv[1:])
