import subprocess
# Put this script in the same directory as docker_tools.py
import docker_tools
import os

# Dictionary with the format "SrrSampleName": "accessionName"
sraAccessionDict = {}

# Dictionary with the format "ErrSampleName": "accessionName"
# Example: ebiAccessionDict = {"ERR418113": "TR00020"}
ebiAccessionDict = {}


# Processes SRA accessions
def sraProcessFile(SRRname, accession):
    # Download fastq
    # You must download sratoolkit and replace the directory below to your fastq-dump binary
    subprocess.call("/Users/awilliams21/Desktop/sratoolkit/bin/fastq-dump --split-3 %s"
                    % (SRRname), shell=True)

    # Rename fastq
    try:
        os.rename("./%s_1.fastq" % (SRRname), "./%s_1.fastq" % (accession))
    except:
        pass
    try:
        os.rename("./%s_2.fastq" % (SRRname), "./%s_2.fastq" % (accession))
    except:
        pass

    # Speedseq align
    # Some notes on the parameters:
    #   -M 3: maximum amount of RAM to use, change this to suit your set up
    #   -R: read group to put in bam file, just leave this as is unless you know what you are doing
    subprocess.call("docker exec -it bio_c sh -c 'cd /bio/ && /speedseq/bin/speedseq align -M 3 -R \"@RG\tID:%s\tSM:%s\tLB:%s\" -o %s %s %s_1.fastq %s_2.fastq'"
                    % (accession, accession, accession, accession, "S_lycopersicum_chromosomes.2.50.fa", accession, accession),
                    shell=True)

    # Lumpy express
    subprocess.call("docker exec -it bio_c sh -c 'cd /bio/ && lumpyexpress -B %s -S %s -D %s'"
                    % (accession + ".bam", accession + ".splitters.bam", accession + ".discordants.bam"),
                    shell=True)

    return


# Same structure as last function, see comments above
def ebiProcessFile(EBIname, accession):
    # Download fastq
    subprocess.call("docker exec -it bio_c sh -c 'cd /bio/ && wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/%s/%s/%s_1.fastq.gz && wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/%s/%s/%s_2.fastq.gz'"
                % (EBIname[0:6], EBIname, EBIname, EBIname[0:6], EBIname, EBIname), shell=True)

    # Rename fastq
    try:
        os.rename("./%s_1.fastq.gz" % (EBIname), "./%s_1.fastq.gz" % (accession))
    except:
        pass
    try:
        os.rename("./%s_2.fastq.gz" % (EBIname), "./%s_2.fastq.gz" % (accession))
    except:
        pass

    # Speedseq align
    subprocess.call("docker exec -it bio_c sh -c 'cd /bio/ && /speedseq/bin/speedseq align -M 3 -R \"@RG\tID:%s\tSM:%s\tLB:%s\" -o %s %s %s_1.fastq.gz %s_2.fastq.gz'"
                    % (accession, accession, accession, accession, "S_lycopersicum_chromosomes.2.50.fa", accession, accession),
                    shell=True)

    # Lumpy express
    subprocess.call("docker exec -it bio_c sh -c 'cd /bio/ && lumpyexpress -B %s -S %s -D %s'"
                    % (accession + ".bam", accession + ".splitters.bam", accession + ".discordants.bam"),
                    shell=True)

    return


# Enter your own mount_directory here. This is where the bams will go
mount_directory = "/Users/awilliams21/Desktop/new_bams/"
docker_tools.check_container_status(mount_directory)

# Installs speedseq in the docker container
subprocess.call("docker exec -it bio_c sh -c 'git clone --recursive https://github.com/hall-lab/speedseq && cd speedseq && make align'",
                shell=True)

for SRRname, accession in sraAccessionDict.items():
    sraProcessFile(SRRname, accession)

for EBIname, acession in ebiAccessionDict.items():
    ebiProcessFile(EBIname, acession)
