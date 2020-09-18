import subprocess
# Put this script in the same directory as docker_tools.py
import docker_tools
import os

# Dictionary with the format "SrrSampleName": "accessionName"
sraAccessionDict = {
#	"SRR7279722": "BGV007878",
#	"SRR7279628": "BGV006865",
#	"SRR7279650": "BGV008108",
#	"SRR7279567": "BGV006906",
#	"SRR7279542": "BGV008095",
#	"SRR7279691": "BGV007894",
#	"SRR7279716": "BGV008065",
#	"SRR7279638": "BGV007198",
#	"SRR7279547": "BGV008224",
#	"SRR7279668": "BGV006235",
#	"SRR7279577": "BGV007936",
#	"SRR7279583": "BGV006370",
#	"SRR7279690": "BGV007895",
#	"SRR7279504": "BGV006363",
#	"SRR7279623": "BGV006327",
#	"SRR7279688": "BGV007870",
#	"SRR7279576": "BGV008354",
#	"SRR7279492": "BGV004584",
#	"SRR7279604": "BGV007920",
#	"SRR7279585": "BGV006825",
#	"SRR7279696": "BGV015380",
#	"SRR7279483": "BGV006148",
#	"SRR7279713": "BGV014508",
#	"SRR7279683": "BGV007109",
#	"SRR7279490": "BGV006208",
#	"SRR7279509": "BGV006175",
#	"SRR7279680": "BGV007901",
#	"SRR7279489": "BGV006229",
#	"SRR7279528": "BGV008051",
	"SRR7279530": "BGV008037"
}

# Dictionary with the format "ErrSampleName": "accessionName"
# Example: ebiAccessionDict = {"ERR418113": "TR00020"}
ebiAccessionDict = {
#	"ERR418071": "EA04939",
#	"ERR418109": "TR00018",
#	"ERR418048": "EA02724",
#	"ERR418114": "EA01037",
#	"ERR418060": "EA00990",
	"ERR418082": "EA00676"
}


# Processes SRA accessions
def sraProcessFile(SRRname, accession):
    # Download fastq
    # You must download sratoolkit and replace the directory below to your fastq-dump binary
    subprocess.call("fastq-dump --split-3 %s"
                    % (SRRname), shell=True)

    # Rename fastq
    try:
        os.rename("./%s_1.fastq" % (SRRname), "./%s_1.fastq" % (accession))
    except:
        subprocess.call("cat ./%s_1.fastq.gz* > ./%s_1.fastq.gz" % (SRRname, accession), shell = True)
    try:
        os.rename("./%s_2.fastq" % (SRRname), "./%s_2.fastq" % (accession))
    except:
        subprocess.call("cat ./%s_2.fastq.gz* > ./%s_2.fastq.gz" % (SRRname, accession), shell = True)

    # Speedseq align
    # Some notes on the parameters:
    #   -M 3: maximum amount of RAM to use, change this to suit your set up
    #   -R: read group to put in bam file, just leave this as is unless you know what you are doing
    subprocess.call("docker exec -i bio_c sh -c 'cd /bio/ && /speedseq/bin/speedseq align -M 20 -R \"@RG\tID:%s\tSM:%s\tLB:%s\" -o %s %s %s_1.fastq %s_2.fastq'"
                    % (accession, accession, accession, accession, "/bio/BGV1.0_genome.fasta", accession, accession),
                    shell=True)

    # Lumpy express
    subprocess.call("docker exec -i bio_c sh -c 'cd /bio/ && lumpyexpress -B %s -S %s -D %s'"
                    % (accession + ".bam", accession + ".splitters.bam", accession + ".discordants.bam"),
                    shell=True)

    return


# Same structure as last function, see comments above
def ebiProcessFile(EBIname, accession):
    # Download fastq
    subprocess.call("docker exec -i bio_c sh -c 'cd /bio/ && wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/%s/%s/%s_1.fastq.gz && wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/%s/%s/%s_2.fastq.gz'"
                % (EBIname[0:6], EBIname, EBIname, EBIname[0:6], EBIname, EBIname), shell=True)

    # Rename fastq
    try:
        os.rename("./%s_1.fastq.gz" % (EBIname), "./%s_1.fastq.gz" % (accession))
    except:
        subprocess.call("cat ./%s_1.fastq.gz* > ./%s_1.fastq.gz" % (EBIname, accession), shell = True)
    try:
        os.rename("./%s_2.fastq.gz" % (EBIname), "./%s_2.fastq.gz" % (accession))
    except:
        subprocess.call("cat ./%s_2.fastq.gz* > ./%s_2.fastq.gz" % (EBIname, accession), shell = True)


    # Speedseq align
    subprocess.call("docker exec -i bio_c sh -c 'cd /bio/ && /speedseq/bin/speedseq align -M 20 -R \"@RG\tID:%s\tSM:%s\tLB:%s\" -o %s %s %s_1.fastq.gz %s_2.fastq.gz'"
                    % (accession, accession, accession, accession, "/bio/BGV1.0_genome.fasta", accession, accession),
                    shell=True)

    # Lumpy express
    subprocess.call("docker exec -i bio_c sh -c 'cd /bio/ && lumpyexpress -B %s -S %s -D %s'"
                    % (accession + ".bam", accession + ".splitters.bam", accession + ".discordants.bam"),
                    shell=True)

    return


# Enter your own mount_directory here. This is where the bams will go
mount_directory = "/home/nathantaitano/Desktop/pimpiSVs/new_bams"
docker_tools.check_container_status(mount_directory)

# Installs speedseq in the docker container
subprocess.call("docker exec -i bio_c sh -c 'git clone --recursive https://github.com/hall-lab/speedseq && cd speedseq && make align'",
                shell=True)

for SRRname, accession in sraAccessionDict.items():
    sraProcessFile(SRRname, accession)

for EBIname, acession in ebiAccessionDict.items():
    ebiProcessFile(EBIname, acession)
