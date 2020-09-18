'''
This script is used in order to convert a vcf into a matrix, which is used
to create a phylogenetic tree. The output matrix.txt and accessions.txt file
can easily be fed to Matlab. See README_external_programs for more detailed
instructions.

Usage:
vcf_to_matrix('/Path/to/master/vcf.vcf', '/Output/directory/location/')
'''


# Creating dictionary entry for every accession to know their groupings
matrixDict = {}
groupingDict = {}
for SPaccession in ["BGV007181",
                    "BGV006775",
                    "BGV007158",
                    "BGV007194",
                    "BGV007109",
                    "BGV007111",
                    "BGV007152",
                    "BGV007161",
                    "BGV007149",
                    "BGV007169",
                    "BGV006370",
                    "TS-419",
                    "TS-438",
                    "TS-416",
                    "BGV015382",
                    "TS-420",
                    "BGV015380",
                    "PAS014479",
                    "TS-156",
                    "BGV006327",
                    "TS-429",
                    "BGV006347",
                    "BGV006353",
                    "BGV006454",
                    "BGV006457",
                    "BGV006336",
                    "TS-411",
                    "TS-421",
                    "BGV006363",
                    "BGV006478",
                    "TS-435",
                    "TS-415",
                    "TS-434",
                    "EA00676",
                    "TS-425",
                    "TS-439",
                    "TS-422",
                    "TS-77",
                    "TS-417",
                    "TS-79",
                    "BGV007151",
                    "BGV007339",
                    "BGV007366",
                    "BGV006208"]:
    matrixDict[SPaccession] = []
    groupingDict[SPaccession] = "SP"
for SLCEcuAccession in ["BGV006229",
                        "BGV006768",
                        "BGV006231",
                        "PI487625",
                        "BGV006767",
                        "PI129026",
                        "BGV006234",
                        "BGV006232",
                        "BGV006792",
                        "BGV006859",
                        "TS-148",
                        "BGV007015",
                        "BGV006901",
                        "BGV006931",
                        "TS-53",
                        "BGV007992",
                        "TS-299",
                        "BGV006867",
                        "BGV005912",
                        "BGV006899",
                        "BGV006907",
                        "TS-413",
                        "BGV006235",
                        "EA06086",
                        "BGV006225",
                        "BGV006934",
                        "BGV012639",
                        "BGV006852",
                        "BGV006904",
                        "BGV008058",
                        "TS-231",
                        "BGV006777",
                        "BGV006881",
                        "BGV006806",
                        "BGV006910",
                        "TS-158",
                        "BGV007023",
                        "BGV006828",
                        "BGV006927",
                        "BGV006175",
                        "BGV006865",
                        "TR00027",
                        "BGV006896",
                        "BGV006906",
                        "BGV012625",
                        "BGV006148",
                        "BGV007017",
                        "PI129033",
                        "BGV006779",
                        "BGV006753"]:
    matrixDict[SLCEcuAccession] = []
    groupingDict[SLCEcuAccession] = "SLC ECU"
for SLCEcuPerSmAccession in ["BGV013161",
                            "BGV008041",
                            "TS-247",
                            "BGV008077",
                            "BGV013945",
                            "BGV008095",
                            "TS-258",
                            "BGV008037",
                            "BGV008225",
                            "TS-273",
                            "TS-56",
                            "TS-57",
                            "BGV006825",
                            "EA00325",
                            "BGV007981",
                            "BGV007989",
                            "PI406890",
                            "BGV008189",
                            "TS-242",
                            "BGV015730",
                            "TS-129",
                            "BGV008096",
                            "BGV012640",
                            "BGV007990",
                            "BGV014515",
                            "BGV014518",
                            "BGV014522",
                            "TS-184",
                            "BGV015727",
                            "BGV015726",
                            "BGV015734",
                            "BGV008065",
                            "BGV014508",
                            "BGV014514",
                            "BGV014519",
                            "TS-304",
                            "BGV008098",
                            "BGV014516"]:
    matrixDict[SLCEcuPerSmAccession] = []
    groupingDict[SLCEcuPerSmAccession] = "SLC ECU-PER-SM"
for SLCMexCaNsaAccession in ["BGV012627",
                            "LA2697",
                            "CATIE-11106-1",
                            "PI129088",
                            "BGV007927",
                            "BGV007934",
                            "BGV007931",
                            "BGV008345",
                            "LA1712",
                            "BGV008354",
                            "BGV004584",
                            "BGV013175",
                            "TS-436",
                            "BGV008108",
                            "BGV008348",
                            "BGV007935",
                            "BGV007933",
                            "BGV008218"]:
    matrixDict[SLCMexCaNsaAccession] = []
    groupingDict[SLCMexCaNsaAccession] = "SLC MEX-CA-NSA"
for SLCMexAccession in ["BGV007911",
                        "BGV007909",
                        "BGV008219",
                        "BGV007910",
                        "BGV007920",
                        "BGV007901",
                        "BGV008223",
                        "TS-69",
                        "BGV007902",
                        "TS-165",
                        "BGV008067",
                        "BGV007908",
                        "BGV008221",
                        "TR00026",
                        "BGV007894",
                        "BGV008070",
                        "TS-154",
                        "BGV013134",
                        "TS-280",
                        "BGV012614",
                        "BGV005895",
                        "TS-229",
                        "BGV007899",
                        "BGV008051",
                        "BGV007918",
                        "BGV007921"]:
    matrixDict[SLCMexAccession] = []
    groupingDict[SLCMexAccession] = "SLC MEX"
for SLLMexAccession in ["EA03362",
                        "LA0767",
                        "BGV007864",
                        "BGV008224",
                        "BGV007867",
                        "EA04939",
                        "BGV007936",
                        "BGV007860",
                        "Voyage",
                        "TS-249",
                        "TS-41",
                        "BGV007871",
                        "TS-131",
                        "BGV007870",
                        "BGV007872"]:
    matrixDict[SLLMexAccession] = []
    groupingDict[SLLMexAccession] = "SLL MEX"
for SLLMajorAccession in ["TS-251",
                        "BGV007857",
                        "TR00022",
                        "TS-141",
                        "BGV007862",
                        "BGV007863",
                        "EA05701",
                        "TS-261",
                        "TR00019",
                        "Tegucigalpa",
                        "BGV007875",
                        "BGV007895",
                        "BGV007878",
                        "BGV007865",
                        "BGV007876",
                        "TS-203",
                        "EA04861",
                        "EA04243",
                        "TS-75",
                        "EA01640",
                        "TR00021",
                        "EA00940",
                        "EA03701",
                        "TS-137",
                        "TS-152",
                        "EA02724",
                        "TR00003",
                        "EA00371",
                        "EA02655",
                        "TS-140",
                        "TS-10",
                        "TS-282",
                        "TS-163",
                        "TS-73",
                        "TS-132",
                        "TS-192",
                        "TS-86",
                        "TR00018",
                        "TS-142",
                        "EA02617",
                        "TS-43",
                        "TS-95",
                        "EA01835",
                        "TS-193",
                        "TS-44",
                        "EA00892",
                        "EA04828",
                        "EA03221",
                        "EA01155",
                        "EA00465",
                        "TR00023",
                        "TS-201",
                        "EA01037",
                        "TS-197",
                        "TR00020",
                        "EA00990",
                        "TS-191",
                        "EA00157",
                        "EA01019",
                        "EA01049",
                        "TS-139",
                        "BGV007854"]:
    matrixDict[SLLMajorAccession] = []
    groupingDict[SLLMajorAccession] = "SLL Major"


# This function is used to remove accessions of a certain threshold
def removeLowCoverageAccessions(depth_file, depth_threshold):
    open_depth_file = open(depth_file, 'r')
    low_coverage_bams = []
    for line in open_depth_file:
        bam_name, read_depth = line.split(':')
        read_depth = float(read_depth)
        if read_depth < depth_threshold:
            bam_name = bam_name.split('.')[0]
            if bam_name.endswith('m'):
                bam_name = bam_name[:-1]
            low_coverage_bams.append(bam_name.split('.')[0])
    return low_coverage_bams

# Uncommemt the following lines and change depth_file to your depth file if
# you want to exclude bams of a certain depth threshold (second parameter of
# removeLowCoverageAccessions is the threshold)
'''depth_file = '/Directory/to/your/depth/file.txt'
low_coverage_bams = removeLowCoverageAccessions(depth_file, 0)
for accession in low_coverage_bams:
    print(accession)
    del matrixDict[accession]
    del groupingDict[accession]
'''


def vcf_to_matrix(masterVcf, output_directory):
    print("Opening %s" % masterVcf)
    vcfReader = open(masterVcf, 'r')

    print("Skipping through header")
    line = vcfReader.readline()
    while line.startswith("#"):
        line = vcfReader.readline()

    print("Parsing master vcf")
    total = 0
    count = 0
    while line:
        if (count >= 100):
            total += count
            count = 0
            print("%i lines parsed" % total)
        cols = line.split('\t')
        try:
            info = cols[7]
        except:
            print("Found invalid line: %s" % line)
            count += 1
            line = vcfReader.readline()
            continue

        try:
            # Attempts to make a list of all the accessions of an SV
            accessionList = info.split("SNAME=")[1].split(";")[0].split(',')
        except:
            print("Invalid line found: %s" % line)
            line = vcfReader.readline()
            continue

        # Some vcf files have extraneous info after the accession name
        # that we have to cut off
        correctedAccessionList = []
        for accession in accessionList:
            correctedAccessionList.append(accession.split(':')[0])
        accessionList = correctedAccessionList

        # For every accession, if the accession has an SV, its matrix gets
        # a 1 appended, otherwise, a 0 is appended
        for accession in matrixDict:
            if accession in accessionList:
                matrixDict[accession].append('1')
            else:
                matrixDict[accession].append('0')

        # Skip a line if this line is a BND (next line will be duplicate)
        if info.split("SVTYPE=")[1].split(';')[0] == "BND":
            vcfReader.readline()
            count += 1

        count += 1
        line = vcfReader.readline()

    vcfReader.close()
    print("Creating matrix files at %s" % (output_directory))
    matrixFile = open(output_directory + "matrix.txt", 'w+')
    accessionFile = open(output_directory + "accessions.txt", 'w+')

    print("Writing to matrix file")
    for accession in matrixDict:
        lineToWrite = '\t'.join(matrixDict[accession]) + '\n'
        matrixFile.write(lineToWrite)
        grouping = groupingDict[accession]

        accessionFile.write(grouping + ' - ' + accession + '\n')

    matrixFile.close()
    accessionFile.close()

    print("Done.")
    return
