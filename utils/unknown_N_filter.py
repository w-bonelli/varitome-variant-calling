import sys, getopt, os
import subprocess
import docker_tools
import random


def unknown_N_filter(input_vcf, output_vcf, reference_genome, v=False,
                        N_threshold=10, flank_rad=50):
    """
    Filters a vcf based on the quality of the reference genome. An SV is
    filtered out if there are more than a certain amount of unknown nucleotide
    bases within a certain amount of base pairs of the SV's endpoints. For
    example, if we input the flank radius to be 50 and the N threshold to 10,
    then if an SV had 15 unknown nucleotides directly before and after its start position
    in the reference genome, then it would be filtered out. The nucleotide
    bases of the reference genome are found using the bedtools nuc command.

    Usage:
    python unknown_N_filter.py -i /vcf/to/be/filtered.vcf -f /reference/fasta/file.fa

    Parameters:
        Required:
            -i: vcf to be filtered
            -f: reference genome in fasta format
                Default: same directory as the input vcf, with _n_filtered.vcf suffix
                IMPORTANT: there must be an index file (.fai) for the reference genome in
                           the same directory as the reference genome. It should be named
                           like so: reference_genome_name.fa.fai
        Optional:
            -o: ouptut vcf
                Default: same directory as the input vcf with "_n_filtered" suffix
            -n: threshold for amount of N in order for an SV to be filtered
                Default: 10
            -r: number of base pairs to fetch nucleotide pairs for
                Default: 50
            -v: verbose mode
            -h: help (display this message)

    Returns a tuple containing a list of clean IDs and a list containing a list of dirty IDs
    """
    mount_directory = os.path.dirname(reference_genome)
    docker_tools.check_container_status(mount_directory)
    mount_directory += '/'

    index_dict = {}
    reference_genome_index_file = reference_genome + ".fai"
    if v: print("Parsing reference genome index at %s" % reference_genome_index_file)
    try:
        open_index_file = open(reference_genome_index_file, 'r')
    except:
        raise Exception("Cannot find index file (.fai) for reference genome in same directory as \
                            reference genome. Try running samtools faidx on the reference genome")
    line = open_index_file.readline()
    while line:
        cols = line.split('\t')
        chr_name = cols[0]
        chr_length = int(cols[1])
        index_dict[chr_name] = chr_length
        line = open_index_file.readline()

    if v: print("Opening %s to create end point flanks" % input_vcf)
    vcf_reader = open(input_vcf, 'r')

    if v: print("Reading through the header")
    line = vcf_reader.readline()
    while line.startswith('#'):
        line = vcf_reader.readline()

    vcf_name = input_vcf.split('/')[-1][:-4]

    random_suffix = str(random.randint(100000,999999))
    bed_name = "temp" + vcf_name + '-' + random_suffix + ".bed"
    bed_file = mount_directory + bed_name

    if v: print("Creating temporary bed file at %s" % bed_file)
    bed_writer = open(bed_file, 'w+')

    while line:
        cols = line.split('\t')
        chr_name = cols[0]
        start_pos = int(cols[1]) - 1
        sv_id = cols[2]
        sv_info = cols[7]

        if ";END=" in sv_info:  # If it is any SV but BND
            end_pos = int(sv_info.split("END=")[1].split(';')[0])
        else:
            end_pos = int(cols[1])

        start_pos_minus_flank = start_pos - flank_rad
        start_pos_plus_flank = start_pos + flank_rad
        end_pos_minus_flank = end_pos - flank_rad
        end_pos_plus_flank = end_pos + flank_rad

        chr_length = index_dict[chr_name]

        if start_pos_minus_flank < 0:
            start_pos_minus_flank = 0
        if end_pos_minus_flank < 0:
            end_pos_minus_flank = 0
        if start_pos_plus_flank > chr_length:
            start_pos_plus_flank = chr_length
        if end_pos_plus_flank > chr_length:
            end_pos_plus_flank = chr_length

        start_pos_minus_flank = str(start_pos_minus_flank)
        start_pos_plus_flank = str(start_pos_plus_flank)
        end_pos_minus_flank = str(end_pos_minus_flank)
        end_pos_plus_flank = str(end_pos_plus_flank)

        bed_writer.write( chr_name + "\t"
                        + start_pos_minus_flank + "\t"
                        + start_pos_plus_flank + "\t"
                        + sv_id + "\n")

        bed_writer.write( chr_name + "\t"
                        + end_pos_minus_flank + "\t"
                        + end_pos_plus_flank + "\t"
                        + sv_id + "\n")

        line = vcf_reader.readline()

    if v: print("%s converted to BED format at %s" % (input_vcf, bed_file))
    vcf_reader.close()
    bed_writer.close()

    fasta_name = reference_genome.split('/')[-1]
    nuc_name = "temp" + vcf_name + '-' + random_suffix + ".nuc"
    nuc_file = mount_directory + nuc_name

    if v: print("Generating nucleotide content at %s" % (nuc_file))
    subprocess.call('docker exec -it bio_c sh -c "bedtools nuc -fi %s -bed %s > %s"'
                    % ("/bio/" + fasta_name, "/bio/" + bed_name, "/bio/" + nuc_name),
                    shell=True)

    os.remove(bed_file)

    if v: print("Parsing nucleotide content")
    open_nuc_file = open(nuc_file, 'r')
    open_nuc_file.readline()    #Skip header
    line = open_nuc_file.readline()

    clean_IDs = []
    bad_IDs = []

    while line:
        cols = line.split('\t')
        id = cols[3]
        N_count = int(cols[10])

        if N_count >= N_threshold:
            if id not in bad_IDs:
                bad_IDs.append(id)
                if id in clean_IDs:
                    clean_IDs.remove(id)
        else:
            if id not in bad_IDs:
                if id not in clean_IDs:
                    clean_IDs.append(id)

        line = open_nuc_file.readline()

    open_nuc_file.close()
    os.remove(nuc_file)

    if v:
        print("Finished parsing nuc content")
        print("Filtering vcf")
    vcf_reader = open(input_vcf, 'r')

    if v: print("Creating filtered vcf file at %s" % output_vcf)
    vcf_writer = open(output_vcf, 'w+')

    line = vcf_reader.readline()
    while line.startswith('#'):
        vcf_writer.write(line)
        line = vcf_reader.readline()

    while line:
        cols = line.split('\t')
        id = cols[2]
        if id in clean_IDs:
            vcf_writer.write(line)

        line = vcf_reader.readline()

    vcf_reader.close()
    vcf_writer.close()

    print("All SVs processed. Filtered vcf at %s" % output_vcf)

    return 0
