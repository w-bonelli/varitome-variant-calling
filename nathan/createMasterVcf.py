import os
import random

'''
This script creaters a master vcf.
The master vcf contains SVs, with the accessions that SV is found in being
 appended to the end of the INFO column. The format is
 SNAME=accession1, accesion2, accession3;

Usage:
createrMasterVcf("/path/to/directory/containing/vcfs/")

The script will crawl through other directories found within the input directory
 looking for vcfs and use those as well.

Note: The script does not yet delete the temp directory after completion, so it
 must be manually deleted before running createMasterVcf again.
'''


def createMasterVcf(input_directory):
    if not (input_directory.endswith("/")):
        input_directory += "/"

    vcf_list = []
    findVcfInDirectory(input_directory, vcf_list)

    # Create dicitonary mapping accessions to their groupings
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
                                "CATIE-11106",
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

    chr_list = ["ch01", "ch02", "ch03", "ch04", "ch05", "ch06",
                "ch07", "ch08", "ch09", "ch10", "ch11", "ch12"]

    del_file_dict = {}
    dup_file_dict = {}
    inv_file_dict = {}
    bnd_file_dict = {}

    del_lines_dict = {}
    dup_lines_dict = {}
    inv_lines_dict = {}
    bnd_lines_dict = {}

    for ch in chr_list:
        del_file_dict[ch] = []
        dup_file_dict[ch] = []
        inv_file_dict[ch] = []
        bnd_file_dict[ch] = []

        del_lines_dict[ch] = {}
        dup_lines_dict[ch] = {}
        inv_lines_dict[ch] = {}
        bnd_lines_dict[ch] = {}

    total_lines = 0

    print("Creating temp directory")
    temp_directory = input_directory + "/tempMasterVcf" + str(random.randint(100000, 999999)) + "/"
    os.mkdir(temp_directory)
    # Loop through every vcf in input_directory
    for vcf in vcf_list:
        vcf_base_name = vcf.split('/')[-1].split('.')[0]
        vcf_temp_directory = temp_directory + vcf_base_name + '/'
        # Creates a directory in the temp directory with vcf name
        try:
            os.mkdir(vcf_temp_directory)
        except:
            continue
        for ch in chr_list:
            # Creates a directory in the vcf directory named after the current chromosome
            os.mkdir(vcf_temp_directory + ch + "/")
            # Creates files for each type of SV in the chromosome directory
            del_file = vcf_temp_directory + ch + "/del"
            dup_file = vcf_temp_directory + ch + "/dup"
            inv_file = vcf_temp_directory + ch + "/inv"
            bnd_file = vcf_temp_directory + ch + "/bnd"
            del_file_dict[ch].append(del_file)
            dup_file_dict[ch].append(dup_file)
            inv_file_dict[ch].append(inv_file)
            bnd_file_dict[ch].append(bnd_file)

        open_vcf_file = open(vcf, 'r')
        line = open_vcf_file.readline()
        # Skip vcf header
        while line.startswith("#"):
            line = open_vcf_file.readline()
        # Skip ch00
        while line.startswith("BGV1.0ch00"):
            line = open_vcf_file.readline()

        # Goes through every line of current vcf and adds each line to the
        # appropriate temporary file.
        for ch in chr_list:
            del_file = vcf_temp_directory + "%s/del" % (ch)
            dup_file = vcf_temp_directory + "%s/dup" % (ch)
            inv_file = vcf_temp_directory + "%s/inv" % (ch)
            bnd_file = vcf_temp_directory + "%s/bnd" % (ch)
            open_del_file = open(del_file, 'w+')
            open_dup_file = open(dup_file, 'w+')
            open_inv_file = open(inv_file, 'w+')
            open_bnd_file = open(bnd_file, 'w+')
            while line.startswith("BGV1.0%s" % ch):
                total_lines += 1
                cols = line.split('\t')
                info_col = cols[7]
                sv_type = info_col.split("SVTYPE=")[1][:3]
                if sv_type == "DEL":
                    open_del_file.write(line)
                elif sv_type == "DUP":
                    open_dup_file.write(line)
                elif sv_type == "INV":
                    open_inv_file.write(line)
                elif sv_type == "BND":
                    open_bnd_file.write(line)
                else:
                    print("Unknown sv type: %s" % sv_type)
                line = open_vcf_file.readline()
            open_del_file.close()
            open_dup_file.close()
            open_inv_file.close()
            open_bnd_file.close()

            # Stores the files in memory to reduce time
            open_del_file = open(del_file, 'r')
            open_dup_file = open(dup_file, 'r')
            open_inv_file = open(inv_file, 'r')
            open_bnd_file = open(bnd_file, 'r')
            del_lines_dict[ch][vcf_base_name] = open_del_file.readlines()
            dup_lines_dict[ch][vcf_base_name] = open_dup_file.readlines()
            inv_lines_dict[ch][vcf_base_name] = open_inv_file.readlines()
            bnd_lines_dict[ch][vcf_base_name] = open_bnd_file.readlines()

    # Create master vcf
    tempVcf = input_directory + "master.vcf"
    openTempVcf = open(tempVcf, 'w+')
    open_vcf_reader = open(vcf_list[0], 'r')

    # Copy header over
    line = open_vcf_reader.readline()
    while line.startswith('#'):
        openTempVcf.write(line)
        line = open_vcf_reader.readline()
    open_vcf_reader.close()

    lines_parsed = 0
    print("Parsing SVs")
    # Loops through every file of each type in their own for loop
    for file_lines_dict in [del_lines_dict, dup_lines_dict, inv_lines_dict]:
        # Likewise for each chromosome
        for ch in chr_list:
            file_dict = file_lines_dict[ch]
            already_checked_svs = []
            for file in file_dict:
                current_lines = file_dict[file]
                print("Parsing SVs in %s" % (file))
                # Loop through every line of a certain vcf of a certain chromosome of a certain sv type
                for line in current_lines:
                    lines_parsed += 1
                    if line in already_checked_svs:
                        continue
                    else:
                        already_checked_svs.append(line)

                    sameSVsAsLineList = [line]
                    accessionsFoundIn = [file]

                    originalCols = line.split('\t')
                    originalInfo = originalCols[7]
                    originalStartPosition = int(originalCols[1])
                    originalEndPosition = int(originalInfo.split("END=")[1].split(';')[0])

                    # Sets the radius of base pairs to compare other SVs to
                    startMin = originalStartPosition - 10
                    startMax = originalStartPosition + 10
                    endMin = originalEndPosition - 10
                    endMax = originalEndPosition + 10

                    # Loop through other files of the same chromosome of the same type (different vcfs)
                    for other_file in file_dict:
                        if file == other_file:
                            continue
                        other_lines = file_dict[other_file]
                        other_lines_length = len(other_lines)

                        # Returns a vcf line if it is the same as the original SV, otherwise returns False
                        sameSv = compareSvToLines(startMin, startMax, endMin, endMax, other_lines, 0, other_lines_length - 1)
                        if sameSv:
                            if sameSv in already_checked_svs:
                                continue
                            sameSVsAsLineList.append(sameSv)
                            accessionsFoundIn.append(other_file)

                    for svLine in sameSVsAsLineList:
                        if not line in already_checked_svs:
                            already_checked_svs.append(svLine)

                    # Find the highest evidence line if there are more than 1 SVs
                    if len(sameSVsAsLineList) > 1:
                        highestEvidence = 0
                        for svLine in sameSVsAsLineList:
                            evidence = int(svLine.split('\t')[9].split(':')[1])
                            if evidence > highestEvidence:
                                bestLine = svLine
                                highestEvidence = evidence
                    else:
                        bestLine = sameSVsAsLineList[0]

                    bestLineCols = bestLine.split('\t')
                    infoCol = bestLineCols[7]
                    if not infoCol.endswith(';'):
                        infoCol += ';'
                    # Append accessions names at the end
                    infoCol += "SNAME=" + ",".join(accessionsFoundIn) + ";"
                    bestLineCols[7] = infoCol
                    bestLine = "\t".join(bestLineCols)

                    openTempVcf.write(bestLine)
                    print("Parsed %i lines out of %i" % (lines_parsed, total_lines))


    # The following block looks through every BND SV
    # This must be seperate from the previous block since BND must be handled differently
    #  as they are in two lines, unlike the other types
    for ch in chr_list:
        file_list = bnd_file_dict[ch]
        already_checked_svs = []
        for file in file_list:
            print("Parsing SVs in %s" % (file))
            copied_file_list = file_list.copy()
            copied_file_list.remove(file)
            open_file = open(file, 'r')
            line = open_file.readline()
            line2 = open_file.readline()
            while line2:
                lines_parsed += 2
                print("Parsed %i lines out of %i" % (lines_parsed, total_lines))
                if line in already_checked_svs:
                    line = open_file.readline()
                    line2 = open_file.readline()
                    continue

                comparisonOutput = compareSVToFilesBND(line, line2, copied_file_list, file)
                sameSVsAsLineList = comparisonOutput[0]
                accessionsFoundIn = comparisonOutput[1]

                for svTuple in sameSVsAsLineList:
                    if not svTuple[0] in already_checked_svs:
                        already_checked_svs.append(svTuple[0])
                if len(sameSVsAsLineList) > 1:
                    highestEvidence = 0
                    for svTuple in sameSVsAsLineList:
                        evidence = int(svTuple[0].split('\t')[9].split(':')[1])
                        if evidence > highestEvidence:
                            bestTuple = svTuple
                            highestEvidence = evidence
                else:
                    bestTuple = sameSVsAsLineList[0]

                bestLine1 = bestTuple[0]
                bestLine2 = bestTuple[1]

                bestLineCols1 = bestLine1.split('\t')
                infoCol1 = bestLineCols1[7]
                if not infoCol1.endswith(';'):
                    infoCol1 += ';'
                infoCol1 += "SNAME=" + ",".join(accessionsFoundIn) + ";"
                bestLineCols1[7] = infoCol1
                bestLine1 = "\t".join(bestLineCols1)

                bestLineCols2 = bestLine2.split('\t')
                infoCol2 = bestLineCols2[7]
                if not infoCol2.endswith(';'):
                    infoCol2 += ';'
                infoCol2 += "SNAME=" + ",".join(accessionsFoundIn) + ";"
                bestLineCols2[7] = infoCol2
                bestLine2 = "\t".join(bestLineCols2)

                openTempVcf.write(bestLine1)
                openTempVcf.write(bestLine2)
                line = open_file.readline()
                line2 = open_file.readline()

            open_file.close()

    openTempVcf.close()
    print("Done.")
    return


# Crawls through a directory and appends all vcfs to vcf_list
def findVcfInDirectory(input_directory, vcf_list):
    if not (input_directory.endswith("/")):
        input_directory += "/"
    file_list = os.listdir(input_directory)
    for file in file_list:
        if file.endswith(".vcf"):
            vcf_list.append(input_directory + file)
        elif os.path.isdir(input_directory + file):
            findVcfInDirectory(input_directory + file, vcf_list)


# Compares a list of lines to the start and end intervals using binary search and recursion
# Returns a vcf line if it is in the intervals, and False if no such line can be found
def compareSvToLines(startMin, startMax, endMin, endMax, lineList, startIdx, endIdx):
    if startIdx > endIdx:
        return False
    midIdx = (startIdx + endIdx) // 2
    line = lineList[midIdx]
    comparisonStart = int(line.split('\t')[1])
    comparisonEnd = int(line.split("END=")[1].split(';')[0])
    if comparisonStart >= startMin and comparisonStart <= startMax:
        if comparisonEnd >= endMin and comparisonEnd <= endMax:
            return line
        else:
            return False
    else:
        if comparisonStart > startMin:
            return compareSvToLines(startMin, startMax, endMin, endMax, lineList, startIdx, midIdx - 1)
        else:
            return compareSvToLines(startMin, startMax, endMin, endMax, lineList, midIdx + 1, endIdx)


# Compares a BND SV to a list of files (linear search), looking for the same SV in other accessions
# Returns a tuple where in the first element is a list of the same SVs as the input SV
#  and the second element is a list of the accessions that the SV was found in.
def compareSVToFilesBND(svToCompare, line2, fileListToCompareTo, sourceFile):
    originalCols = svToCompare.split('\t')
    originalInfo = originalCols[7]
    originalStartPosition = int(originalCols[1])
    originalEndPosition = int(line2.split('\t')[1])

    # Sets the radius intervals
    originalStartMin = originalStartPosition - 10
    originalStartMax = originalStartPosition + 10
    originalEndMin = originalEndPosition - 10
    originalEndMax = originalEndPosition + 10

    sameSvs = [(svToCompare, line2)]
    accession = sourceFile.split('/')[-3]
    # Cleans the accession name if it ends in 'm' (happens if bam was merged)
    if accession.endswith('m'):
        accession = accession[:-1]
    accessionsFoundIn = [accession]

    for file in fileListToCompareTo:
        open_file = open(file, 'r')
        accessionOfFile = file.split('/')[-3]
        if accessionOfFile.endswith('m'):
            accessionOfFile = accessionOfFile[:-1]
        line = open_file.readline()
        next_line = open_file.readline()
        while next_line:
            if int(line.split('\t')[1]) < originalStartPosition - 30:
                line = open_file.readline()
                next_line = open_file.readline()
                continue
            if int(line.split('\t')[1]) > originalStartPosition + 30:
                open_file.close()
                break
            # calls the compareSvsBND to find SV in other accessions
            comparisonOutput = compareSvsBND(line, line2, originalStartMin, originalStartMax, originalEndMin, originalEndMax)
            if comparisonOutput:
                sameSvs.append((line, line2))
                accessionsFoundIn.append(accessionOfFile)
                open_file.close()
                break
            line = open_file.readline()
            next_line = open_file.readline()
        open_file.close()
    return (sameSvs, accessionsFoundIn)


# Compares two BND SV lines to the the start and end intervals
# Returns True if they are the same SV, or False otherwise
def compareSvsBND(comparisonSv, comparisonSv2, originalStartMin, originalStartMax, originalEndMin, originalEndMax):
    comparisonCols = comparisonSv.split('\t')
    comparisonInfo = comparisonCols[7]
    comparisonStartPosition = int(comparisonCols[1])
    comparisonEndPosition = int(comparisonSv2.split('\t')[1])

    if ((comparisonStartPosition >= originalStartMin and comparisonStartPosition <= originalStartMax)
        and (comparisonEndPosition >= originalEndMin and comparisonEndPosition <= originalEndMax)):
        return True
    else:
        return False
