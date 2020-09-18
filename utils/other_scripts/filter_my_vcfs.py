import os
import unknown_N_filter
import remove_chr00
import filter_vcfs

def findVcfInDirectory(input_directory, vcf_list):
    if not (input_directory.endswith("/")):
        input_directory += "/"
    file_list = os.listdir(input_directory)
    for file in file_list:
        if file.endswith(".vcf"):
            vcf_list.append(input_directory + file)
        elif os.path.isdir(input_directory + file):
            findVcfInDirectory(input_directory + file, vcf_list)

depth_file = "/Users/awilliams21/Desktop/find_SVs/bamdepths.txt"
open_depth_file = open(depth_file, 'r')
depth_dict = {}
for line in open_depth_file:
    accession, depth = line.split(':')
    depth_dict[accession] = depth

newDirectory = "/Users/awilliams21/Desktop/2018 Summer NSF/Filtered VCF/"
tempDirectory = "/Users/awilliams21/Desktop/2018 Summer NSF/temp/"
vcfList = []
findVcfInDirectory("/Users/awilliams21/Desktop/2018 Summer NSF/Unfiltered VCF/", vcfList)
for vcf in vcfList:
    print("Filtering %s" % vcf)
    location = vcf.split("/Unfiltered VCF/")[1]
    base_name = location.split('.')[0]

    output_location = newDirectory + base_name + ".filtered.vcf"
    if os.path.exists(output_location):
        print("Already filtered, moving on")
        continue

    print("   Removing ch00")
    temp_output1 = tempDirectory + base_name + ".1.vcf"
    remove_chr00.remove_chr00(vcf, temp_output1)

    print("   Evidence filter")
    temp_output2 = tempDirectory + base_name + ".2.vcf"
    filter_vcfs.filter_vcfs(temp_output1, temp_output2, depth_dict)

    print("   N filtering")
    unknown_N_filter.unknown_N_filter(temp_output2, output_location, "/Users/awilliams21/Documents/tomatoes/S_lycopersicum_chromosomes.2.50.fa")

    print(" Done with %s" % vcf)

print("DONE.")
