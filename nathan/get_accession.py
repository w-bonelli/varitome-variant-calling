import os, sys, getopt
import subprocess
import random
import docker_tools

usage = """
Outputs the accession of a bam file. The accession is also output
to a text file specified by -o. 

Will not find the accession of a bam file already listed in the output
text file.

Usage:
python get_accession.py -i /path/to/input/bam -o /optional/acession/list/file

Parameters:
    Required:
        -i: bam file to find the accession of
    Optional:
        -o: text file (.txt) where the accession will be output to. Will
            also be parsed to check if the bam file has already been
            processed.
            Default: accession_list.txt in the same directory as the input
                     bam
        -q: accession will not be output to text file at all (quiet)
        -v: verbose mode
        -h: help (display this messge)
"""

def get_accession(bam_input, accession_file=None, q=False, v=False):
    mount_directory = os.path.dirname(bam_input)
    docker_tools.check_container_status(mount_directory)
    mount_directory += '/'
    
    bam_input_name = bam_input.split('/')[-1]
    already_parsed = False
    if not q:
        if accession_file is not None and accession_file.endswith(".txt"):
            if v: print("Checking if %s has already been parsed" % bam_input)
            open_accession_file = open(accession_file, 'r+')
            line = open_accession_file.readline()
            while line:
                bam_name = line.split(':')[0]
                if bam_input_name == bam_name:
                    already_parsed = True
                line = open_accession_file.readline()
            open_accession_file.close()
        else:
            accession_file = mount_directory + "accession_file.txt"
            if os.path.exists(accession_file):
                if v: print("Checking if %s has already been parsed" % bam_input)
                open_accession_file = open(accession_file, 'r+')
                line = open_accession_file.readline()
                while line:
                    bam_name = line.split(':')[0]
                    if bam_input_name == bam_name:
                        already_parsed = True
                    line = open_accession_file.readline()
                open_accession_file.close()

        if already_parsed:
            print("\n%s has already been parsed. Its accession is in %s\n"
                    % (bam_input, accession_file))
            return 1
        
        if v: print("Opening accession file at %s" % accession_file)
        accession_file_exists = os.path.exists(accession_file)
        open_accession_file = open(accession_file, "a+")

    #Prepare temp file info
    base_name = bam_input_name[0:-4]
    random_suffix = str(random.randint(100000,999999))
    temp_file_base_name = "temp" + base_name + '-' + random_suffix
    temp_file = mount_directory + temp_file_base_name

    if v: print("Creating temporary file at %s" % temp_file)
    open_temp_file = open(temp_file, 'x')
    open_temp_file.close()
    
    #Write input bam's header to temp file
    subprocess.call("docker exec -it bio_c sh -c 'samtools view -H %s > %s'"
                    % ("/bio/" + bam_input_name, "/bio/" + temp_file_base_name), 
                    shell=True)
 
    if v: print("Parsing bam header for accession information")
    accession = None
    open_temp_file = open(temp_file, 'r')
    line = open_temp_file.readline()
    #Get to the @RG line where SM: is
    while line and not line.startswith("@RG"):
        line = open_temp_file.readline()
    
    try:
        SM_substring = line.split("SM:")[1]
    except:
        print("\nAccession could not be found. BAM file header may be corrupt?\n")
        return 2

    accession = SM_substring.split('\t')[0]
    
    open_temp_file.close()
    os.remove(temp_file)
    
    if not q:
        open_accession_file.write(bam_input_name + ':' + accession + '\n')
        open_accession_file.close()

    print("\nThe accession of %s is %s" % (bam_input, accession))
    if not q:
        print("Accession written to %s\n" % accession_file)

    return(accession)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "i:o:qvh")
    except:
        print(usage + "\nGetOptError\n")
        return
    needed = ['-i']

    #Set default values for arguments
    bam_input = None
    accession_file = None
    verbose = False
    quiet = False

    #Assign arguments
    for opt, arg in opts:
        if opt == '-h':
            print(usage); return
        elif opt == '-v':
            verbose = True
        elif opt == '-i':
            bam_input = arg
        elif opt == '-o':
            accession_file = arg
        elif opt == '-q':
            quiet = True

    #Check if all required parameters were given
    for opt, arg in opts:
        if opt in needed:
            needed.remove(opt)
    if needed:
        print(usage)
        for missing in needed:
            print("Error: " + {
                '-i': "Input bam file required (-i /bam/file/to/be/parsed.bam)"
                }[missing])
            print('')
            return

    # -----

    get_accession(bam_input, accession_file=accession_file, q=quiet, v=verbose)

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
