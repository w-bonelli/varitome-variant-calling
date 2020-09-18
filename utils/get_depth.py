import sys, os, getopt
import subprocess
import random

usage = """
Finds the average read depth of a bam file. The average read depth is found
by taking the output of `samtools depth -a` (depth at all positions) and storing
it in a temporary file. Then, the average of every position's read depth is found
and printed, as well as saved to a text file, which can be specified with -o.

Usage:
python get_depth.py -i /path/to/input/bam -o /optional/depth/text/file 

Parameters:
    Required:
        -i: bam file to find the read depth of
    Optional:
        -o: text file (.txt) where average read depth will be output to. Will
            also be parsed to check if this bam has already been processed.
            Default: <input file name stripped of .bam extension>.txt in the same directory as the input bam.
        -h: help (display this message)
"""


def get_depth(bam_file, depth_file):
    if os.path.exists(depth_file):
        raise ValueError(f"Output file '{depth_file}' already exists")

    print(f"Getting read depth of {bam_file}")

    accession = bam_file.split('/')[-1][0:-4]
    temp_file = f"temp_{accession}_{str(random.randint(100000, 999999))}"

    with open(temp_file, 'x') as temp, open(depth_file, "a+") as output:
        subprocess.call(f"singularity exec bio_c.sif sh -c 'samtools depth -a {bam_file} > {temp_file}'", shell=True)
        depth_sum = 0
        position = 0

        for line in temp:
            read_depth = int(line.split('\t')[2])
            depth_sum += read_depth
            position += 1

        os.remove(temp_file)

        mean_depth = depth_sum / position
        output.write(accession + ".bam:" + str(mean_depth) + '\n')

        print(f"Mean read depth of '{bam_file}' is {mean_depth}")
        return 0


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'i:o:hv')
    except getopt.GetoptError:
        print(usage + "\nGetOptError\n");
        return
    needed = ['-i']

    input_file = None
    output_file = None

    # Assign arguments
    for opt, arg in opts:
        if opt == '-h':
            print(usage);
            return
        elif opt == '-i':
            input_file = arg
        elif opt == '-o':
            output_file = arg

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

    get_depth(input_file, output_file)

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
