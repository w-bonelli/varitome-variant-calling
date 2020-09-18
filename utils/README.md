<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [find_SVs](#find_svs)
  - [Dependencies](#dependencies)
    - [python 3.0 or higher](#python-30-or-higher)
    - [docker](#docker)
  - [Using main.py](#using-mainpy)
  - [Understanding individual commands and their files](#understanding-individual-commands-and-their-files)
    - [docker_tools.py](#docker_toolspy)
      - [get_mount_location](#get_mount_location)
      - [restart_docker_container(mount_directory)](#restart_docker_containermount_directory)
      - [check_container_status(mount_directory)](#check_container_statusmount_directory)
    - [merge_bams.py](#merge_bamspy)
      - [get_accession.py](#get_accessionpy)
      - [merge_bam_list.py](#merge_bam_listpy)
    - [get_depth.py](#get_depthpy)
    - [get_vcfs.py](#get_vcfspy)
    - [remove_chr00.py](#remove_chr00py)
    - [unknown_N_filter](#unknown_n_filter)
    - [get_known_data.py](#get_known_datapy)
    - [filter_vcfs.py](#filter_vcfspy)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# find_SVs
find_Svs is a program that acts as a pipeline for finding structural variants. The program is designed to do the following:
1. merge BAM files
2. get BAM files' average read depth
3. get VCF files from BAM files
4. filter out VCF calls made in poorly mapped regions of the reference genome
5. remove chromosome 00 SV calls (based on reads are not anchored to any location in the refernce genome)
6. find SV calls in the VCF files that are known to be true/false so that their evidence can be analyzed for filtering purposes.
7. filter the SV calls made in the VCF files
8. rescue breakends that were thrown away because they did not pass the filter so long as their mate passed

Please note that currently this program is based on a unix file path system and will not run properly on a Windows machine. In the future, Windows compatiability could be developed.

## Dependencies

   ### python 3.0 or higher
   This script utilizes some python3 syntax and commands. 

   ### docker
   This script uses the container platform [Docker][1], which allows one to run specific images on any computer through the cloud. In this case, it's flexibility is being utilized in order to forgo installing an extensive list of prerequisites in order to run various bioinformatics tools. The true strength of this approach becames apparent when many files must be processed, which can be incredibly time intensive. The docker image can be initialized very quickly on many computers to allow for the processing to be spread out and sped up. These tools are helpful in performing structural variant analysis and are as follows:

   * To Merge BAM files
       * [samtools][2] - Can merge BAM files together (samtools merge).
       * [picard][3] - Can change the header of a bam file to match other bam files, which is required for them to be merged (picard AddOrReplaceReadGroups).
   * To get read depth
       * [samtools][4] - Can output the read depth at every position of a bam file (samtools depth -a).
   * To Generate VCF files
       * [Lumpy][5] - A structural variant caller that integrates evidence from read-pairs, split-reads, read-depth, and prior knowledge. Here we are using Lumpy Express with its default parameters.
   * To analyze VCF files
       * [pysam][6] - A python module for reading and manipulating files in BAM format (samtools wrapper)
       * [numpy][7] - A python module for reading and manipulating files in BAM format (samtools wrapper)
       * [scipy][8] - A python module for reading and manipulating files in BAM format (samtools wrapper)
   * To filter based on reference genome quality
       * [bedtools][9] - Can find the nucleotide content of the reference genome at a specific feature (bedtools nuc).
   * To filter VCF files

   In order to get the best performance and speeds possible, make sure to increase the resource limits within docker. This can be done by navigating to "Preferences" and then "Advanced" within docker. Increases these limits will not mean that these resources will constantly be allocated and taken by docker, but rather those resources are allowed to be accessed and used when needed.

## Using main.py
Used to call any of the functions associated with find_SVs. Use of main is recommended as opposed to running any of the functions individually (however, we have tried to make each file self-contained). The main program takes the following functions and options:

   functions:
   ```
   merge_bams
   get_depth
   get_vcfs
   unknown_N_filter
   remove_chr00
   get_known_data
   filter_vcfs
   rescue_mates
   all
   ```
   Note that main will not call a function more than once in a single function (use a directory for the same effect). Nor will main allow a user to call another command with the all command (which is precautionary).
   Opts:
   ```
   -i : input file or directory (merge_bams requires a directory)
   -o : path for output file or directory (must be the same type as the input)
   -d : read depth file (for format, see below)
   -t : true positive file (for format, see below)
   -f : false positive file (for format, see below)
   ```
Called alone, each function are requires use of the following opts:
* ```merge_bams``` - ```-i```
* ```get_depth``` - ```-i```
* ```get_vcfs``` - ```-i```
* ```remove_chr00``` - ```-i```
* ```get_known_data``` - ```-i -d -t -f```
* ```filter_vcfs``` - ```-i -d```
* ```all``` - ```-i -d -t -f```

Please note that main will automatically fill in missing arguments for chained function calls when it can (which is why no function requires an output path).
* If input is missing, main will take the last output of the necessary type (if it exists). For example:
   ```
   python3 find_SVs/main.py get_vcfs -i Desktop/bams/ -o Desktop/vcfs_are_cool/ remove_chr00
   ```
   This command will call remove_chr00 with its input as ```Desktop/vcfs_are_cool/```
* If output is missing, main will take the directory containing the input file or directory and create a folder or file based off contained within the same directory. Depending on the function called and assuming a directory is inputted, the directory generated will be in the parent directory of the input and be called one of the following: merged_bams, vcfs, no00_vcfs, or filtered_vcfs. get_depths and get_known_data do not generated directories, only files-- which will be contained in the parent directory of the input file. If you have a directory in your working directory that has the same name as one of the default directories above, do not use the default names unless you do not mind your directory being overwritten. For individual files, output names will be the name of the input file with one of the follow suffixes appended: ".bam", ".vcf", "_no00.vcf", "_known_data_tp.txt"/"_known_data_fp.txt", "_filtered.vcf".
. For example:
   ```
   python3 find_SVs/main.py get_vcfs -i Desktop/bams/ remove_chr00
   ```
   This command will call get_vcfs with its output as ```Desktop/vcfs/```. This output will automatically be piped into remove_chr00 as an input.
* If read depth file is missing, main will check the previously called commands to see if they have a read depth file. If multiple commands have a read depth file, then the read depth file of the function call furtherest down in the pipeline (see list of commands) will be used. If there is only one such file, then that file will be used.
For example:
   ```
   python3 find_SVs/main.py get_known_data -i Desktop/vcfs/ -d Desktop/read_depths.txt filter_vcfs
   ```
   ```
   python3 find_SVs/main.py get_depths -i Desktop/bams/ filter_vcfs
   ```
   Both of these commands will pass filter_vcfs a depth file. The first will pass ```Desktop/read_depths.txt```, and the second will pass ```Desktop/bams_read_depths.txt``` (which is named using the default process).
* True positive and false positive files cannot be auto-filled as they can only be called once in a command.

When main exits it will return a number. The meaning of potential exit codes are as follows:

     0 - ran successfully
     1 - does not recognize the function called by the command line.
     2 - no function was called.
     3 - does not recognize an option that was specified.
     4 - user specified that they wanted to run all functions but also specific functions.
     5 - function called more than once. This is not supported due to the methods by which empty parameter fields
     are filled in (i.e. it would not make sense for a filter_vcf call to take a filtered vcf as its input).
     6 - missing an original input file; the first function has no input file.
     7 - missing an original read depth file; the first function that requires read depth has no read depth file.
     8 - missing an original true positive file; the first function that requires false positives has no false
     positives file.
     9 - missing an original false positive file; the first function that requires true positives has no true
     positives file.


## Understanding individual commands and their files
   ### docker_tools.py
   Contains three functions related to the docker container. 
   
   #### get_mount_location
   Function that checks where the docker container is currently mounted.
   
   Example Standalone Function Call:
   ```
   docker_tools.get_mount_location()
   ```
           Returns the current mount directory
  
   #### restart_docker_container(mount_directory)
   Function that restarts the docker container and sets the mount directory.
   
   Example Standalone Function Call:
   ```
   docker_tools.restart_docker_container(mount_directory)
   ```
           mount_directory : str - path of the directory to be mounted
           
   #### check_container_status(mount_directory)
   Checks if the docker container is correctly configured and running. If not, restarts the docker container with the proper configuration. check_container_status is the most important of these three functions. It is used in main.py, but also standalone to ensure the docker image is properly configured.

   Example Standalone Function Call:
   ```
   docker_tools.restart_docker_container(mount_directory)
   ```
           mount_directory : str - path of the directory to be mounted
           
   ### merge_bams.py
   Merges bam files of the same accession together using SAMtools. The accession of a bam is found using get_accession.py. These bam files are ran through picard AddOrReplaceReadGroups in order to ensure they have the same header.
   All bam files located in the input directory (does not walk through) are parsed.

   Example Command:
   ```
   python3 find_SVs/main.py merge_bams -f /directory/containing/first_set_of_bams -s /directory/containing/second_set
   ```

   Example Stand Alone Function call
   ```
   merge_bams(input_directory, output_directory=None, accession_file=None, v=False, k=False)
   ```
           input_directory : str - path of the directory in which to search for mergable bam files
           output_directory : str - path of the directory where all merged bams (and bams that did not need to be merged) will be output to. Please note that output bams that have been merged will have a name with m appended right before ".bam".
           accession_file : str - path to a previously generated accession file 
           v : Bool - Validity of the statement: I should operate in verbose mode
           k : Bool - Validity of the statement: I should keep temporary file containing samtools depth output for every
               position of the bam file
               (WARNING: this file will be around 20GB)

   #### get_accession.py
   This script is called by merge_bams in order to find bam files of the same accession.
   Outputs the accession of a bam file. This is found by parsing the header and finding what follows the SM: field. The accession is stored as follows:
   ```
   <file>:<accession name>\n
   ```
   Where the file name might be something like HGV007901-1.bam and the accession HGV007901

   Example Command:
   ```
   python3 find_SVs/get_accession.py -i /bam/accesion/tobefound.bam
   ```

   Example Stand Alone Function call
   ```
   get_accession(input_bam, accession_file, q, v)
   ```
           bam_input : str - path of the bam file to find the accession of
           accession_file : str - path of the text file (.txt) where the accession will be written to. Will
               also be parsed to check if this bam has already been processed.
           q : Bool - Validity of the statement: I should operate in quiet mode (not write anything to any accession file)
           v : Bool - Validity of the statement: I should operate in verbose mode

   #### merge_bam_list.py
   This script is called by merge_bams to merge a list of bams.
   Outputs a merged bam file, merged using SAMtools merge.

   Example Standalone Funciton Call
   ```
   merge_bam_list(bam_list, output_directory, accession, v, k)
   ```
           bam_list : str - list of paths of bam files to be merged
           output_directory : str - path of the directory for the merged bam to be placed in       
           accession : str - name of the accession of the bams to be merged
           k : Bool - Validity of the statement: I should keep temporary file containing samtools depth output for every
               position of the bam file
               WARNING: this file will be around 20GB
           v : Bool - Validity of the statement: I should operate in verbose mode


   ### get_depth.py
   Calls SAMtools to find the read depth at every position in a BAM file and stores these in a temporary file. These read depths are then averaged out and stored in a text file. This is done for every bam in a given directory (does not walk through). The average read depth of a BAM is stored as follows:
   ```
   file_name:read_depth
   ```
   Where the file name might be something like HGV007901.bam and read depth may be like 20.4211. At the end of each line there is a new line character.

   Example Command:
   ```
   python3 find_SVs/main.py get_depths -i /directory/containing/bams -o /directory/bam_depths.txt
   ```

   Example Stand Alone Function call
   ```
   get_depth(bam_file, depth_file, k, v)
   ```
           bam_file : str - path of the bam file to find the read depth of
           depth_file : str - path of the text file (.txt) where average read depth will be output to. Will
               also be parsed to check if this bam has already been processed.
           k : Bool - Validity of the statement: I should keep temporary file containing samtools depth output for every
               position of the bam file
               WARNING: this file will be around 20GB
           v : Bool - Validity of the statement: I should operate in verbose mode


   ### get_vcfs.py
   Calls LumpyExpress. A VCF file containing the structural variants predicted by Lumpy is produced for every BAM file in the given input directory. Note: this program does not walk through directories.

   Example Command:
   ```
   python3 find_SVs/main.py get_vcfs -i /directory_containing_bams
   ```

   Example Stand Alone Function call
   ```
   get_vcfs(input_bam_file, output_vcf_path)
   ```
           input_bam_file : str - path of the BAM file to get a VCF from.
           output_vcf_path : str - Desired output path for the VCF file.

   ### remove_chr00.py
   Reads a VCF file containing the structural variants predicted by Lumpy and creates a copy of the VCF that has all chromosome 00 structural variants removed (including breakends whose patners map to chr00). Note: this program does not walk through directories.

   Example Command:
   ```
   python3 find_SVs/main.py remove_chr00 -i /directory_containing_vcfs
   ```

   Example Stand Alone Function call
   ```
   remove_chr00(input_vcf, output_vcf_path)
   ```
           input_vcf : str - path of the VCF file to base new VCF file on.
           output_vcf_path : str - Desired output path for the VCF file without chr00.

   ### unknown_N_filter
   Filters a vcf based on the quality of the reference genome. An SV is filtered out if there are more than a certain amount of unknown nucleotide bases within a certain amount of base pairs of the SV's endpoints. For example, if we input the flank radius to be 50 and the N threshold to 10, then if an SV had 15 unknown nucleotides directly before and after its start position in the reference genome, then it would be filtered out. The nucleotide bases of the reference genome are found using the bedtools nuc command.

   Example Command:
   ```
   python3 find_SVs/unknown_N_filter.py -i /vcf/to/be/filtered.vcf -f /reference/fasta/file.fa
   ```

   Example Stand Alone Function call
   ```
   unknown_N_filter(input_vcf, reference_genome, output_vcf, N_threshold, flank_rad, v)
   ```
           input_vcf : str - path of the vcf file to be filtered
           reference_genome : str - path of the reference genome in fasta format (.fa) (Must be indexed)
           output_vcf : str - path of the directory where the filtered vcf file should go
           N_threshold : int - the number of Ns necessary in the flank for the SV to be filtered out
           flank_rad : int - the number of base pairs to check for Ns around the SV endpoints
           v : Bool - Validity of the statement: I should operate in verbose mode


   ### get_known_data.py
   Takes the user's known strucutral variants and searches all VCF files to find true positive and false positive calls. A call is consider a true positive if it meets the follow criteria:
   1. The 95% confidence interval for the call's position includes the known SV's position
   2. If the call is not a break end, the 95% confidence interval for the call's end position includes the known SV's end position
   3. The call's structural variant type matches the structural variant type or types of the known SV or it is a break end.
   A call is consider a false positive if it meets the follow criteria:
   1. The 95% confidence interval for the call's position includes the known false SV's position
   2. If the call is not a break end, the 95% confidence interval for the call's end position includes the known false SV's end position
   3. The call's structural variant type matches the structural variant type or types of the known false SV or it is a break end.

   Example Command:
   ```
   python3 find_SVs/main.py get_known_data -i /directory_containing_bam -d /depth_file.txt -t /known_true_svs.txt -f /known_false_svs.txt
   ```

   Example Stand Alone Function call
   ```
   get_known_data(input_vcf, output, depth_dict, true_positive_dict, false_positive_dict, overwrite)
   ```
           input_vcf : str - path of the VCF files to find calls in (directory or single file)
           output : str - Desired output path for directory containing two text files (see below)
           depth_dict : dict - Dictionary containing the read-depths of all accessions in the input
           true_positive_dict : dict - Dictionary containing all structural varients known to be true
           false_positive_dict : dict - Dictionary containing all structural varients known to be false
           overwrite : bool - Validity of the statement: if a directory exists where I want my output to go, I should overwrite it.

   All true positives are written to one file and all false positives are written to another file. These files are not written in VCF file format. Rather they are written as in the format:
   ```
   file    read depth    actual type    call type    validated pos    validated end    predicted pos (95% CI)    predicted end (95% CI)    total evidence    PE evidence    SR evidence    PE:SR ratio    Imprecise?
   ```
   This format is used so that the data can be easily analyzed in Excel or with other programs. Currently, the process of filtering VCF files is not particularily well established (especially for Lumpy VCFs). Generally, the advice given is that one ought to require some amount of split-read evidence and some amount of paired-end evidence and that the bounds for the number of reads (SR or PE) required ought to be related to the read depth of a given file. Ryan Layer (the founder of Lumpy) has commented on this issue [several times][10][11][12]. As of yet, we have not be able to get SVTyper to work. The files generated by get_known_data, are designed to order to attempt to find trends that differentiate Lumpy's true positive calls and its false positive calls. Here is some example data that we were able to generate from tomato accessions:

   ![Err: Image not found](https://github.com/egoetz/find_SVs/blob/master/example/example_data.png "Example Data")

   Please note that this is a small subset of a number of tomato accessions. It cannot be used as a representation of all BAM files. Another example of this type of data analysis can be found in Figure 6 of ["LUMPY: a probabilistic framework for structural variant discovery."][13] The intent of creating a program for user-driven filtering is to allow for possible differing factors in the genetic data being processed to naturally come to light (it is not clear that all VCFs should be filtered the same way). By observing the distribution of one's data, one can avoid using a filter that may only work for a specific data set.

   ### filter_vcfs.py
   Takes the user's VCF files and filters them based on certain criteria. Right now the filtering criteria is hard coded and an SV is required to meet the following standards:
   1. Must have at least one piece of PE evidence.
   2. Must have at least one piece of SR evidence.
   3. The amount of SR evidence must be less than or equal to the amount of PE evidence.
   4. The total SU evidence for all other SVs must be greater than or equal to (average read depth) / 2.
   5. The total SU evidence for all other SVs must be less than or equal to 3 * (average read depth).

   Example Command:
   ```
   python3 find_SVs/main.py filter_vcfs -i /directory_containing_bam -d /depth_file.txt
   ```

   Example Stand Alone Function call
   ```
   filter_vcfs(input_vcf, output_vcf_path, average_depth_dict)
   ```
           input_vcf : str - path of the VCF file to filter
           output_vcf_path : str - Desired output path for filtered VCF file
           average_depth_dict : dict - Dictionary containing the read-depths of accession in the input
        


[1]: https://www.docker.com/what-docker "Docker Website"
[2]: http://www.htslib.org "Samtools Website"
[3]: https://github.com/broadinstitute/picard "picard"
[4]: http://www.htslib.org "Samtools Website"
[5]: https://github.com/arq5x/lumpy-sv "Lumpy GitHub"
[6]: https://github.com/pysam-developers/pysam "Pysam GitHub"
[7]: http://www.numpy.org "Numpy Website"
[8]: https://www.scipy.org "SciPy Website"
[9]: https://github.com/arq5x/bedtools2 "bedtools GitHub"
[10]: https://github.com/arq5x/lumpy-sv/issues/108 "Layer 1"
[11]: https://github.com/arq5x/lumpy-sv/issues/231 "Layer 2"
[12]: https://groups.google.com/forum/#!topic/lumpy-discuss/gO_6e6s5Xbs "Layer 3"
[13]: https://genomebiology.biomedcentral.com/articles/10.1186/gb-2014-15-6-r84#Sec10 "Lumpy Paper"
