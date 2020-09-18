import os


def avg_read_depth(bam_file, depth_file):
    accession = bam_file.split('/')[-1][0:-4]
    output_file = f"{accession}.depth.average.txt"

    if not os.path.exists(bam_file):
        raise ValueError(f"BAM file '{bam_file}' does not exist")

    if not os.path.exists(depth_file):
        raise ValueError(f"Read depth file '{depth_file}' does not exist")

    if os.path.exists(output_file):
        raise ValueError(f"Output file '{output_file}' already exists")

    print(f"Getting average read depth of '{bam_file}'...")

    with open(depth_file, 'r') as depth, open(output_file, "a+") as output:
        depth_sum = 0
        position = 0

        for line in depth:
            read_depth = int(line.split('\t')[2])
            depth_sum += read_depth
            position += 1

        mean_depth = depth_sum / position
        output.write(accession + ".bam:" + str(mean_depth) + '\n')
        print(f"Average read depth of '{bam_file}' is {mean_depth}.")

