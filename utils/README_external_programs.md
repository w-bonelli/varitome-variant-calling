This document contains documentation on external programs used, as well as various
tips and tricks in performing these analyses learned over Summer 2018.

External programs used:
speedseq
lumpyexpress
samtools
matlab
docker
picard
bedtools

Indexing the reference genome with samtools:
  > samtools faidx <reference.fa>

Creating a phylogenetic tree:
  1. Generate a master vcf using createMasterVcf.py
  2. Use vcf_to_matrix.py with this master vcf
  3. Open Matlab and drag the vcf_to_matirx.py output files (matrix.txt, accessions.txt)
      into the "Current Folder" tab in Matlab (far left tab)
  4. Type the following commands into the command window:
      > load('matrix.txt')
      > accessions = importdata('accessions.txt')
      > tree = linkage(matrix, 'average', 'jaccard')
      > dend = dendrogram(tree, 255, 'Labels', accessions, 'Orientation', 'left', 'ColorThreshold', .90)
          Note: the second number (in our example, 255) must be as large as the
            amount of accessions being analyzed. Play around with the number
            following 'ColorThreshold' for better coloring.

    If you have a lot of accessions being analyzed, the accessions labels on the figure
      will be far too large. To fix this, type the following commands
        > set(gca, 'FontSize', 4)
          Play around with the number following 'FontSize' to suit your data set.

    Make sure you maximize the figure window on your screen and save as .svg for
    best results.


Now, some tips and tricks:

Docker:
  The name of our container is always 'bio_c'
  We store all the files in the mounted directory /bio/ in the container
  When starting scripts involving docker containers, they may stall at the very
    beginning. An easy solution is to just restart the script
  Here are some useful commands:
    If you want to check on the container's status:
      > docker ps -a
    If you want to run a command in the container's bash
      > docker exec -it bio_c sh -c "insert command here"
    If you want to attach your terminal to the container's
      > docker exec -it bio_c bash
      You can run the usual commands from here, such as 'ls', 'cd', etc
    If the container needs a hard reset
      > docker stop bio_c
      > docker rm bio_c

Running new programs:
  The world of bioinformatics is very confusing for the uninitiated, especially
  when it comes to the abundance of programs and their dependencies.
  Installing all these dependencies is quite the process. The dockerfile found in
  /docker/dockerfile creates an image that has all the prereq dependencies installed
  for everything our scripts require. This saves A LOT of work and allows you to
  quickly process files on other computers. In the future, new programs will need
  to be run. I highly suggest just installing these through a docker image as your
  life will be much easier. In a 8 week research project, installing all these
  dependencies without the dockerfile could take upwards of a week, which is precious
  time.

Downloading bams online:
  Sometimes you may have to download bams from SRA or EBI to complete your data
  set. The processFile script in other_scripts/ may aid in doing this. See that
  folder's README as well as the following notes.
  Downloading SRA accessions (accessions that start with TS):
    Search https://www.ncbi.nlm.nih.gov/sra with the accession name (for example, "TS-10")
    Click on the sample you want to download
    Navigate down to where it says "Runs" and has a small table.
    Copy the value under "Run" in the table. It should look like "SRR1572461" or similar.
    Paste this value in the sraAccessionDict in processFile.py as a key.
    For the value, enter your accession name.
    After doing this for all your bams, start the script.

  Downloading EBI accessions (accessions start with EA or TR):
    Search https://www.ebi.ac.uk/ena with the accession name (for example, "TR00028")
    Click on the sample you want to download.
    Navigate to the table at the bottom of the page.
    Copy the value under "Run accession".
    Paste this value in the ebiAccessionDict in processFile.py as a key.
    For the value, enter your accession name.
    After doing this for all your bams, start the script.

  You can process both EBI and SRA accessions at the same time.

  The standalone command for SRA accessions is
    >> sratoolkit/bin/fastq-dump --split-3 SRRXXXXXXX
  See other_scripts/processFile.py for the standalone command for EBI accessions
    (It is way more complicated)

  Use speedeq align for alignment
