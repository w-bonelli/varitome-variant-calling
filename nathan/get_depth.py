import sys, os, getopt
import subprocess
import random
import docker_tools

usage = """
Outputs the average read depth of a bam file. The average read depth is found
by taking the output of samtools depth -a (depth at all positions) and storing
it in a temp file. Then, the average of every position's read depth is found
and printed, as well as output to a text file, which can be specified with -o.

Will not calculate depths already found in the optional depth text file (-o)

Usage:
python get_depth.py -i /path/to/input/bam -o /optional/depth/text/file 

Parameters:
    Required:
        -i: bam file to find the read depth of
    Optional:
        -o: text file (.txt) where average read depth will be output to. Will
            also be parsed to check if this bam has already been processed.
            Default: bamdepths.txt in the same directory as the input bam.
        -k: keep temporary file containing samtools depth output for every
            position of the bam file
            WARNING: this file will be around 20GB
        -v: verbose mode
        -h: help (display this message)
"""


def get_depth(bam_file, depth_file=None, k=False, v=False):
    mount_directory = os.path.dirname(bam_file)
    docker_tools.check_container_status(mount_directory)
    mount_directory += '/'

    already_parsed = False
    if depth_file is not None and depth_file.endswith(".txt") and os.path.exists(depth_file):
        if v: print("Checking if %s has already been parsed" % bam_file)
        open_depth_file = open(depth_file, 'r')
        line = open_depth_file.readline()
        while line:
            bam_name = line.split(':')[0]
            if bam_file.split('/')[-1] == bam_name:
                already_parsed = True
            line = open_depth_file.readline()
        open_depth_file.close()
    else:
        depth_file = mount_directory + "bamdepths.txt"
        if os.path.exists(depth_file):
            open_depth_file = open(depth_file, 'r')
            line = open_depth_file.readline()
            while line:
                bam_name = line.split(':')[0]
                if bam_file.split('/')[-1] == bam_name:
                    already_parsed = True
                line = open_depth_file.readline()
            open_depth_file.close()

    if already_parsed:
        print("\n%s has already been parsed. Its read depth is in %s\n" 
                % (bam_file, depth_file))
        return 1
    
    if v: print("Opening depth file at %s" % depth_file)
    depth_file_exists = os.path.exists(depth_file)
    open_depth_file = open(depth_file, "a+")
    
    if v: print("Getting read depth of %s" % bam_file)
    #Prepare temp file info
    accession = bam_file.split('/')[-1][0:-4]
    random_suffix = str(random.randint(100000,999999))
    temp_file_base_name = 'temp' + accession + '-' + random_suffix
    temp_file = mount_directory + temp_file_base_name

    #Create temp file
    open_temp_file = open(temp_file, 'x')
    open_temp_file.close()

    #Write every read's depth to temp file
    subprocess.call("singularity exec bio_c.sif sh -c 'samtools depth -a %s > %s'"
                     % ("/bio/" + accession + ".bam", "/bio/" + temp_file_base_name), 
                     shell=True)

    open_temp_file = open(temp_file, 'r')
    sum_of_read_depths = 0
    position_count = 0
    for line in open_temp_file:
        read_depth = int(line.split('\t')[2])
        sum_of_read_depths += read_depth
        position_count += 1
    open_temp_file.close()

    if not k:
        os.remove(temp_file)

    average_read_depth = sum_of_read_depths / position_count
    open_depth_file.write(accession + ".bam:" + str(average_read_depth) + '\n')

    open_depth_file.close()
    
    print("\nAverage read depth of %s is %f" % (bam_file, average_read_depth))
    print("Average read depth written to %s\n" % depth_file)
    return 0


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'i:o:hvk')
    except getopt.GetoptError:
        print(usage + "\nGetOptError\n");
        return
    needed = ['-i']

    #Set default values for arguments
    input_bam = None
    output_depth_file = None
    verbose = False
    keep_temp_file = False

    #Assign arguments
    for opt, arg in opts:
        if opt == '-h':
            print(usage); return
        elif opt == '-v':
            verbose = True
        elif opt == '-k':
            keep_temp_file = True
        elif opt == '-i':
            input_bam = arg
        elif opt == '-o':
            output_depth_file = arg

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

    get_depth(input_bam, depth_file=output_depth_file, v=verbose, k=keep_temp_file)

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
