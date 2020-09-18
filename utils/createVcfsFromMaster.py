'''
This script contains functions to generate VCFs to answer the 3 questions
proprosed in Summer 2018

When trying to input groupings, only the following are accepted (exactly as seen here)
"SP", "SLC ECU", "SLC ECU-PER-SM", "SLC MEX-CA-NSA", "SLC MEX", "SLL MEX", "SLL Major"
'''

# Create dictionary entries for every accessions, (key = accession, value = grouping)
accessionGroupingDict = {}
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
                    "TR00028",
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
    accessionGroupingDict[SPaccession] = "SP"
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
    accessionGroupingDict[SLCEcuAccession] = "SLC ECU"
for SLCEcuPerSmAccession in ["BGV013161",
                            "BGV008041",
                            "EA00027",
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
    accessionGroupingDict[SLCEcuPerSmAccession] = "SLC ECU-PER-SM"
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
                            "EA05170",
                            "BGV008218"]:
    accessionGroupingDict[SLCMexCaNsaAccession] = "SLC MEX-CA-NSA"
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
    accessionGroupingDict[SLCMexAccession] = "SLC MEX"
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
    accessionGroupingDict[SLLMexAccession] = "SLL MEX"
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
                        "EA01854",
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
                        "AlisaCraig",
                        "TS-142",
                        "EA02617",
                        "TS-43",
                        "Moneymaker",
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
                        "EA00448",
                        "TR00020",
                        "EA00990",
                        "TS-191",
                        "EA05581",
                        "EA00157",
                        "EA01019",
                        "EA01049",
                        "EA01088",
                        "TS-139",
                        "BGV007854"]:
    accessionGroupingDict[SLLMajorAccession] = "SLL Major"

amountAccessionsDict = {"SP": 45,
                        "SLC ECU": 50,
                        "SLC ECU-PER-SM": 88,
                        "SLC MEX-CA-NSA": 19,
                        "SLC MEX": 26,
                        "SLL MEX": 15,
                        "SLL Major": 61}

totalAmountAccessions = 254


# This function takes a master vcf line as a parameter and returns a dictionary
# containing accessions that this SV is found in
def getDataFromLine(line):
    cols = line.split('\t')
    try:
        info = cols[7]
        # Creates a list of every accession of this line
        accessionList = info.split("SNAME=")[1].split(";")[0].split(',')
    except:
        return "SKIP"

    # Some lines have extraneous info after accession that needs to be cleaned up
    correctedAccessionList = []
    for accession in accessionList:
        correctedAccessionList.append(accession.split(':')[0])
    accessionList = correctedAccessionList

    groupingDict = {"SP": [],
                    "SLC ECU": [],
                    "SLC ECU-PER-SM": [],
                    "SLC MEX-CA-NSA": [],
                    "SLC MEX": [],
                    "SLL MEX": [],
                    "SLL Major": []}

    for accession in accessionList:
        if accession.endswith('m'):
            accession = accession[:-1]
        grouping = accessionGroupingDict[accession]
        groupingDict[grouping].append(accession)

    return groupingDict


# Writes a standardized header to an open vcf file
# (Needed because some vcf have crazy headers after a lot of processing)
def writeVcfHeader(open_vcf):
    open_vcf.writelines(
    '''##fileformat=VCFv4.2
##source=LUMPY
##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">
##INFO=<ID=SVLEN,Number=.,Type=Integer,Description="Difference in length between REF and ALT alleles">
##INFO=<ID=END,Number=1,Type=Integer,Description="End position of the variant described in this record">
##INFO=<ID=STRANDS,Number=.,Type=String,Description="Strand orientation of the adjacency in BEDPE format (DEL:+-, DUP:-+, INV:++/--)">
##INFO=<ID=IMPRECISE,Number=0,Type=Flag,Description="Imprecise structural variation">
##INFO=<ID=CIPOS,Number=2,Type=Integer,Description="Confidence interval around POS for imprecise variants">
##INFO=<ID=CIEND,Number=2,Type=Integer,Description="Confidence interval around END for imprecise variants">
##INFO=<ID=CIPOS95,Number=2,Type=Integer,Description="Confidence interval (95%) around POS for imprecise variants">
##INFO=<ID=CIEND95,Number=2,Type=Integer,Description="Confidence interval (95%) around END for imprecise variants">
##INFO=<ID=MATEID,Number=.,Type=String,Description="ID of mate breakends">
##INFO=<ID=EVENT,Number=1,Type=String,Description="ID of event associated to breakend">
##INFO=<ID=SECONDARY,Number=0,Type=Flag,Description="Secondary breakend in a multi-line variants">
##INFO=<ID=SU,Number=.,Type=Integer,Description="Number of pieces of evidence supporting the variant across all samples">
##INFO=<ID=PE,Number=.,Type=Integer,Description="Number of paired-end reads supporting the variant across all samples">
##INFO=<ID=SR,Number=.,Type=Integer,Description="Number of split reads supporting the variant across all samples">
##INFO=<ID=BD,Number=.,Type=Integer,Description="Amount of BED evidence supporting the variant across all samples">
##INFO=<ID=EV,Number=.,Type=String,Description="Type of LUMPY evidence contributing to the variant call">
##INFO=<ID=PRPOS,Number=.,Type=String,Description="LUMPY probability curve of the POS breakend">
##INFO=<ID=PREND,Number=.,Type=String,Description="LUMPY probability curve of the END breakend">
##ALT=<ID=DEL,Description="Deletion">
##ALT=<ID=DUP,Description="Duplication">
##ALT=<ID=INV,Description="Inversion">
##ALT=<ID=DUP:TANDEM,Description="Tandem duplication">
##ALT=<ID=INS,Description="Insertion of novel sequence">
##ALT=<ID=CNV,Description="Copy number variable region">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=SU,Number=1,Type=Integer,Description="Number of pieces of evidence supporting the variant">
##FORMAT=<ID=PE,Number=1,Type=Integer,Description="Number of paired-end reads supporting the variant">
##FORMAT=<ID=SR,Number=1,Type=Integer,Description="Number of split reads supporting the variant">
##FORMAT=<ID=BD,Number=1,Type=Integer,Description="Amount of BED evidence supporting the variant">
''')
    return


def question1(masterVcf, output_directory):
    vcfReader = open(masterVcf, 'r')
    SPVcfWriter = open(output_directory + "allSP.vcf", 'w+')
    SLCEcuVcfWriter = open(output_directory + "allSLCEcu.vcf", 'w+')
    SLCEPSVcfWriter = open(output_directory + "allSLCEcuPerSm.vcf", 'w+')
    SLCMCNVcfWriter = open(output_directory + "allSLCMexCaNsa.vcf", 'w+')
    SLCMexVcfWriter = open(output_directory + "allSLCMex.vcf", 'w+')
    SLLMexVcfWriter = open(output_directory + "allSLLMex.vcf", 'w+')
    SLLMajorVcfWriter = open(output_directory + "allSLLMajor.vcf", 'w+')

    vcfWriterDict = {"SP": SPVcfWriter,
                    "SLC ECU": SLCEcuVcfWriter,
                    "SLC ECU-PER-SM": SLCEPSVcfWriter,
                    "SLC MEX-CA-NSA": SLCMCNVcfWriter,
                    "SLC MEX": SLCMexVcfWriter,
                    "SLL MEX": SLLMexVcfWriter,
                    "SLL Major": SLLMajorVcfWriter}

    line = vcfReader.readline()
    # Write header to output vcf
    while line.startswith("##"):
        line = vcfReader.readline()

    for grouping in vcfWriterDict:
        writeVcfHeader(vcfWriterDict[grouping])

    # Write last header line to output vcf
    lastHeaderLine = line.split('\n')[0]
    lastHeaderLine += '\t' + "AMOUNT OF %s ACCESSIONS FOUND IN" % grouping + '\t' + "%s ACCESSIONS FOUND IN" % grouping + '\n'
    for grouping in vcfWriterDict:
        vcfWriterDict[grouping].write(lastHeaderLine)

    count = 0
    total = 0
    line = vcfReader.readline()
    # Parse the rest of the lines
    while line:
        if count == 100:
            total += count
            count = 0
            print("%i lines read" % total)
        groupingDict = getDataFromLine(line)
        if groupingDict == "SKIP":
            print("Found an invalid line: %s" % line)
            count += 1
            line = vcfReader.readline()
            continue
        for grouping in groupingDict:
            # 50 accessions are duplicated in both SLC ECU-PER-SM and SLC-ECU.
            # Those 50 accessions are only found in the SLC ECU dictionary entry,
            # so we must copy those accessions over if the grouping we are looking
            # at is SLC ECU-PER-SM
            if grouping == "SLC ECU-PER-SM":
                for accession in groupingDict["SLC ECU"]:
                    groupingDict[grouping].append(accession)
            # If the current grouping has at least 1 accessions that has this SV
            if len(groupingDict[grouping]) > 0:
                accessions = groupingDict[grouping]
                amountAccessions = len(accessions)
                totalAmountAccessionsInGrouping = amountAccessionsDict[grouping]
                newLine = line.split('\n')[0] + '\t' + "%i/%i" % (amountAccessions, totalAmountAccessionsInGrouping) + '\t' + ", ".join(accessions) + '\n'
                vcfWriterDict[grouping].write(newLine)
        count += 1
        line = vcfReader.readline()

    vcfReader.close()
    for grouping in vcfWriterDict:
        vcfWriterDict[grouping].close()

    print("Question 1 done.")
    return


def question2(masterVcf, output_directory):
    vcfReader = open(masterVcf, 'r')
    SPVcfWriter = open(output_directory + "onlySP.vcf", 'w+')
    SLCEcuVcfWriter = open(output_directory + "onlySLCEcu.vcf", 'w+')
    SLCEPSVcfWriter = open(output_directory + "onlySLCEcuPerSm.vcf", 'w+')
    SLCMCNVcfWriter = open(output_directory + "onlySLCMexCaNsa.vcf", 'w+')
    SLCMexVcfWriter = open(output_directory + "onlySLCMex.vcf", 'w+')
    SLLMexVcfWriter = open(output_directory + "onlySLLMex.vcf", 'w+')
    SLLMajorVcfWriter = open(output_directory + "onlySLLMajor.vcf", 'w+')

    vcfWriterDict = {"SP": SPVcfWriter,
                    "SLC ECU": SLCEcuVcfWriter,
                    "SLC ECU-PER-SM": SLCEPSVcfWriter,
                    "SLC MEX-CA-NSA": SLCMCNVcfWriter,
                    "SLC MEX": SLCMexVcfWriter,
                    "SLL MEX": SLLMexVcfWriter,
                    "SLL Major": SLLMajorVcfWriter}

    line = vcfReader.readline()
    # Write header to output vcf
    while line.startswith("##"):
        line = vcfReader.readline()

    for grouping in vcfWriterDict:
        writeVcfHeader(vcfWriterDict[grouping])

    # Write last header line to output vcf
    lastHeaderLine = line.split('\n')[0]
    lastHeaderLine += '\t' + "AMOUNT OF %s ACCESSIONS FOUND IN" % grouping + '\t' + "%s ACCESSIONS FOUND IN" % grouping + '\n'
    for grouping in vcfWriterDict:
        vcfWriterDict[grouping].write(lastHeaderLine)

    count = 0
    total = 0
    line = vcfReader.readline()
    # Parse the rest of the lines
    while line:
        if count == 100:
            total += count
            count = 0
            print("%i lines read" % total)
        groupingDict = getDataFromLine(line)
        if groupingDict == "SKIP":
            print("Found an invalid line: %s" % line)
            count += 1
            line = vcfReader.readline()
            continue
        amountGroupingsWithAccessions = 0

        # Loops through every group and if the SV is found in that grouping,
        # then amountGroupingsWithAccessions is increased by 1
        for grouping in groupingDict:
            if len(groupingDict[grouping]) > 0:
                amountGroupingsWithAccessions += 1

        # We will only continue if the amount of groupings that the SV is found
        # in is 1
        if amountGroupingsWithAccessions == 1:
            # Finds which grouping has the SV
            for grouping in groupingDict:
                if len(groupingDict[grouping]) > 0:
                    accessions = groupingDict[grouping]
                    amountAccessions = len(accessions)
                    totalAmountAccessionsInGrouping = amountAccessionsDict[grouping]
                    newLline = line.split('\n')[0] + '\t' + "%i/%i" % (amountAccessions, totalAmountAccessionsInGrouping) + '\t' + ", ".join(accessions) + '\n'
                    vcfWriterDict[grouping].write(newLline)
        count += 1
        line = vcfReader.readline()

    vcfReader.close()
    for grouping in vcfWriterDict:
        vcfWriterDict[grouping].close()

    print("Question 2 done.")
    return


def question3(masterVcf, grouping1, grouping2, output_directory):
    vcfReader = open(masterVcf, 'r')
    # Standardized input
    groupingFileNameDict = {"SP": "SP",
                            "SLC ECU": "SLCEcu",
                            "SLC ECU-PER-SM": "SLCEcuPerSm",
                            "SLC MEX-CA-NSA": "SLCMexCaNsa",
                            "SLC MEX": "SLCMex",
                            "SLL MEX": "SLLMex",
                            "SLL Major": "SLLMajor"}
    bothGroupingsVcfWriter = open(output_directory + "%sAnd%s.vcf" % (groupingFileNameDict[grouping1], groupingFileNameDict[grouping2]), 'w+')
    grouping1VcfWriter = open(output_directory + "%sWithout%s.vcf" % (groupingFileNameDict[grouping1], groupingFileNameDict[grouping2]), 'w+')
    grouping2VcfWriter = open(output_directory + "%sWithout%s.vcf" % (groupingFileNameDict[grouping2], groupingFileNameDict[grouping1]), 'w+')

    vcfWriters = [bothGroupingsVcfWriter, grouping1VcfWriter, grouping2VcfWriter]

    line = vcfReader.readline()
    # Write header to output vcf
    while line.startswith("##"):
        for vcfWriter in vcfWriters:
            vcfWriter.write(line)
        line = vcfReader.readline()

    for vcfWriter in vcfWriters:
        writeVcfHeader(vcfWriter)

    # Write last header line to output vcf
    lastHeaderLine = line.split('\n')[0]
    lastHeaderLine1 = lastHeaderLine + '\t' + "AMOUNT OF %s ACCESSIONS FOUND IN" % grouping1 + '\t' + "%s ACCESSIONS FOUND IN" % grouping1 + '\n'
    lastHeaderLine2 = lastHeaderLine + '\t' + "AMOUNT OF %s ACCESSIONS FOUND IN" % grouping2 + '\t' + "%s ACCESSIONS FOUND IN" % grouping2 + '\n'
    lastHeaderLineBoth = lastHeaderLine + '\t' + "AMOUNT OF %s ACCESSIONS FOUND IN" % grouping1 + '\t' + "%s ACCESSIONS FOUND IN" % grouping1 + '\t' + "AMOUNT OF %s ACCESSIONS FOUND IN" % grouping2 + '\t' + "%s ACCESSIONS FOUND IN" % grouping2 + '\n'
    grouping1VcfWriter.write(lastHeaderLine1)
    grouping2VcfWriter.write(lastHeaderLine2)
    bothGroupingsVcfWriter.write(lastHeaderLineBoth)

    count = 0
    total = 0
    line = vcfReader.readline()
    # Parse the rest of the lines
    while line:
        if count == 100:
            total += count
            count = 0
            print("%i lines read" % total)
        groupingDict = getDataFromLine(line)
        if groupingDict == "SKIP":
            print("Found an invalid line: %s" % line)
            count += 1
            line = vcfReader.readline()
            continue

        if grouping1 == "SLC ECU-PER-SM":
            for accession in groupingDict["SLC ECU"]:
                groupingDict[grouping1].append(accession)
        elif grouping2 == "SLC ECU-PER-SM":
            for accession in groupingDict["SLC ECU"]:
                groupingDict[grouping2].append(accession)


        amountGroupingsWithAccessions = 0
        inGrouping1 = False
        inGrouping2 = False
        if len(groupingDict[grouping1]) > 0:
            inGrouping1 = True
        if len(groupingDict[grouping2]) > 0:
            inGrouping2 = True

        if inGrouping1 and inGrouping2:
            accessions1 = groupingDict[grouping1]
            accessions2 = groupingDict[grouping2]
            amountAccessions1 = len(accessions1)
            amountAccessions2 = len(accessions2)
            totalAmountAccessionsInGrouping1 = amountAccessionsDict[grouping1]
            totalAmountAccessionsInGrouping2 = amountAccessionsDict[grouping2]
            line = line.split('\n')[0] + '\t' + "%i/%i" % (amountAccessions1, totalAmountAccessionsInGrouping1) + '\t' + ", ".join(accessions1) + '\t' + "%i/%i" % (amountAccessions2, totalAmountAccessionsInGrouping2) + '\t' + ", ".join(accessions2) + '\n'
            bothGroupingsVcfWriter.write(line)
        elif inGrouping1:
            accessions = groupingDict[grouping1]
            amountAccessions = len(accessions)
            totalAmountAccessionsInGrouping = amountAccessionsDict[grouping1]
            line = line.split('\n')[0] + '\t' + "%i/%i" % (amountAccessions, totalAmountAccessionsInGrouping) + '\t' + ", ".join(accessions) + '\n'
            grouping1VcfWriter.write(line)
        elif inGrouping2:
            accessions = groupingDict[grouping2]
            amountAccessions = len(accessions)
            totalAmountAccessionsInGrouping = amountAccessionsDict[grouping2]
            line = line.split('\n')[0] + '\t' + "%i/%i" % (amountAccessions, totalAmountAccessionsInGrouping) + '\t' + ", ".join(accessions) + '\n'
            grouping2VcfWriter.write(line)

        count += 1
        line = vcfReader.readline()

    vcfReader.close()
    for vcfWriter in vcfWriters:
        vcfWriter.close()

    print("Question 3 done.")
    return
