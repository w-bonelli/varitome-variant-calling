import sys, os, getopt
import subprocess
import random
from pathlib import Path

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
    if os.path.exists(depth_file):
        raise ValueError(f"Output file '{depth_file}' already exists")

    print(f"Getting read depth of {bam_file}")

    accession = bam_file.split('/')[-1][0:-4]
    random_suffix = str(random.randint(100000,999999))
    temp_file = 'temp' + accession + '-' + random_suffix

    with open(temp_file, 'x') as temp, open(depth_file, "a+") as output:
	    subprocess.call("singularity exec bio_c.sif sh -c 'samtools depth -a %s > %s'"
			     % (bam_file, temp_file), 
			     shell=True)

	    sum_of_read_depths = 0
	    position_count = 0
	    for line in temp:
		read_depth = int(line.split('\t')[2])
		sum_of_read_depths += read_depth
		position_count += 1

	    if not k:
		os.remove(temp_file)

	    average_read_depth = sum_of_read_depths / position_count
	    output.write(accession + ".bam:" + str(average_read_depth) + '\n')
	    
	    print(f"Average read depth of '{bam_file}' is {average_read_depth}")
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
