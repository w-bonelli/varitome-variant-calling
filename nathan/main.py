import sys
import getopt
import os
from collections import Counter
import merge_bams
import get_depth
import get_vcfs
import remove_chr00
import unknown_N_filter
import get_known_data
import filter_vcfs


def main(args):
    """
    Main program called in order to run any of the vcf scripts.
    Usage:  python main.py [function_called] -i <bam file directory>
    :param: args
        Required command line input:
            [function_called] - Input the function_called you would like to perform from the following list:
                    get_vcfs - generates vcfs from bam files
                    remove_chr00 - filters out chr00 and chr00's breakend partners
                    get_known_data - finds the evidence distribution of vcf files
                    filter_vcfs - filters out SVs based on evidence
                    all - performs all of the above functions
            -i <file or directory> = Input the file or directory to be examined or parsed.
             Please note that if one would like to run more than one command, then one ought to input the base
             directory with all of the files contained directly therein. Currently, this program is not designed to
             walk through the main directory to find files based on extensions as it seems unneccessary and we do not
             want to have users accidentally run lumpy on a bunch of forgotten, hidden bam files. However, this may be
             changed.
        Additional Requirements for specific functions:
            get_known_data & all
                -d <read depth file> = Input the file to be search through for the read depth. Each line in the file
                should be formatted as follows: "<file name>.bam:<read depth>\n"
                -t <true positive file> = Input the file that contains all SVs known to exist and be true. This file
                should be formatted as follows: "<start chromosome>:<start position>:<end chromosome><end position>
                <SV type>:<potential other SV type (complex event)>"
                Please note that you may add as many SV types as you would like.
                -f <false positive file> = Input the file that contains all SVs known not to exist. This file
                should be formatted as follows: "<start chromosome>:<start position>:<end chromosome><end position>
                <SV type>:<potential other SV type (complex event)>"
                Please note that you may add as many SV types as you would like.
            filter_vcfs
                -d <read depth file> = Input the file to be search through for the read depth. Each line in the file
                should be formatted as follows: "<file name>.bam:<read depth>\n"


    :return: Number indicating whether main ran successfully.
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
    """

    subcommands = [
        ("merge_bams", []),
        ("get_depth", []),
        ("get_vcfs", []),
        ("remove_chr00", []),
        ("unknown_N_filter", []),
        ("get_known_data", []),
        ("filter_vcfs", []),
        ("all", [])
    ]

    start = -1
    last_matching_index = -1
    is_function_called = False
    for i in range(len(subcommands)):
        j = 0
        while j in range(len(args)):
            if not args[j].startswith('-'):
                if args[j] not in [pair[0] for pair in subcommands] and args[j].find('/') == -1:
                    print("Error: Invalid function called.")
                    print(main.__doc__)
                    return 1
                if subcommands[i][0] == args[j]:
                    is_function_called = True
                    if start != -1 and last_matching_index != -1:
                        for arg in args[start:j]:
                            subcommands[last_matching_index][1].append(arg)
                    start = j + 1
                    last_matching_index = i
                    break
            j += 1
        if i == len(subcommands) - 1:
            for arg in args[start:]:
                subcommands[last_matching_index][1].append(arg)
    if not is_function_called:
        print("You must select at least one function.")
        return 2

    for pair in subcommands:
        if len(pair[1]) == 0:
            continue
        function_called = pair[0]
        try:
            opts, args = getopt.getopt(pair[1], 'i:o:d:t:f:r:h')
        except getopt.GetoptError:
            print("Error: Invalid command line option.")
            print(main.__doc__)
            return 3

        input = ''
        output = ''
        reference = ''
        depth_file = ''
        true_positive_dict = {}
        false_positive_dict = {}
        multiplicity = Counter([pair[0] for pair in opts])
        if list(filter(lambda a: a != 0 and a != 1, multiplicity.values())):
            print("Error: an option was repeated. for multiple files, please use directories.")
            return 3.5
        for opt, arg in opts:
            if opt == '--h':
                print(main.__doc__)
            elif opt == '-i':
                if arg.find(os.getcwd()) == -1:
                    if arg.startswith('/'):
                        input = os.getcwd() + arg
                    else:
                        input = os.getcwd() + '/' + arg
                else:
                    input = arg
                if input.endswith('/'):
                    input = input[:-1]
            elif opt == '-o':
                if arg.find(os.getcwd()) == -1:
                    output = os.getcwd() + '/' + arg
                else:
                    output = arg
                if function_called == "get_depth" or function_called == "get_known_data" and os.path.isdir(output):
                    print("Error: get_depth and get_known_data cannot take a directory as an output.")
                    return 10
            elif opt == '-r':
                if arg.find(os.getcwd()) == -1:
                    if arg.startswith('/'):
                        reference = os.getcwd() + arg
                    else:
                        reference = os.getcwd() + '/' + arg
                else:
                    reference = arg
                if not os.path.isfile(reference):
                    print("Error: The reference file must be a file.")
                    return 10
            elif opt == '-d':
                if arg.find(os.getcwd()) == -1:
                    depth_file = os.getcwd() + '/' + arg
                else:
                    depth_file = arg
                if not os.path.isfile(depth_file):
                    print("Error: The depth file must be a file.")
                    return 10
            elif opt == '-t':
                if arg.find(os.getcwd()) == -1:
                    true_positive_file = os.getcwd() + '/' + arg
                else:
                    true_positive_file = arg
                if not os.path.isfile(true_positive_file):
                    print("Error: The provided true positive file must be a file.")
                    return 10
                reading_true_positive = open(true_positive_file)
                true_positive_dict = {}
                line = reading_true_positive.readline()
                while line:
                    info = line.split(':')
                    true_positive_dict[info[0] + '.' + info[1]] = [info[2] + '.' + info[3]]
                    for left in info[4:]:
                        if left.endswith('\n'):
                            left = left[:left.rfind('\n')]
                        true_positive_dict[info[0] + '.' + info[1]].append(left)
                    line = reading_true_positive.readline()
                reading_true_positive.close()
            elif opt == '-f':
                if arg.find(os.getcwd()) == -1:
                    false_positive_file = os.getcwd() + '/' + arg
                else:
                    false_positive_file = arg
                if not os.path.isfile(false_positive_file):
                    print("Error: The provided false positive file must be a file.")
                    return 10
                reading_false_positive = open(false_positive_file)
                false_positive_dict = {}
                line = reading_false_positive.readline()
                while line:
                    info = line.split(':')
                    false_positive_dict[info[0] + '.' + info[1]] = [info[2] + '.' + info[3]]
                    for left in info[4:]:
                        if left.endswith('\n'):
                            left = left[:left.rfind('\n')]
                        false_positive_dict[info[0] + '.' + info[1]].append(left)
                    line = reading_false_positive.readline()
                reading_false_positive.close()

        if function_called == "merge_bams":
            pair[1].clear()
            pair[1].append(input)
            pair[1].append(output)
        elif function_called == "get_depth":
            pair[1].clear()
            pair[1].append(input)
            pair[1].append(output)
        elif function_called == "get_vcfs":
            pair[1].clear()
            pair[1].append(input)
            pair[1].append(output)
        elif function_called == "remove_chr00":
            pair[1].clear()
            pair[1].append(input)
            pair[1].append(output)
        elif function_called == "unknown_N_filter":
            pair[1].clear()
            pair[1].append(input)
            pair[1].append(output)
            pair[1].append(reference)
        elif function_called == "get_known_data":
            pair[1].clear()
            pair[1].append(input)
            pair[1].append(output)
            pair[1].append(depth_file)
            pair[1].append(true_positive_dict)
            pair[1].append(false_positive_dict)
        elif function_called == "filter_vcfs":
            pair[1].clear()
            pair[1].append(input)
            pair[1].append(output)
            pair[1].append(depth_file)
        elif function_called == "all":
            pair[1].clear()
            pair[1].append(input)
            pair[1].append(output)
            pair[1].append(depth_file)
            pair[1].append(reference)
            pair[1].append(true_positive_dict)
            pair[1].append(false_positive_dict)

    if not ("all", []) in subcommands and not (("merge_bams", []) in subcommands and ("get_depth", []) in subcommands
            and ("get_vcfs", []) in subcommands and ("remove_chr00", []) in subcommands and
            ("get_known_data", []) in subcommands and ("filter_vcfs", []) in subcommands):
        print("Please clarify your command. Would you like to run all processes or %s" %
              ([pair[0] for pair in subcommands].remove("all")))
        return 4
    if not ("all", []) in subcommands:
        # merge_bams
        subcommands[0][1].append(subcommands[7][1][0])
        subcommands[0][1].append('')

        # get_depth
        subcommands[1][1].append('')
        subcommands[1][1].append('')

        # get_vcfs
        subcommands[2][1].append('')
        subcommands[2][1].append('')

        # unknown_N_filter
        subcommands[3][1].append('')
        subcommands[3][1].append('')
        subcommands[3][1].append(subcommands[7][1][3])
        print(subcommands[3][1])

        # remove_chr00
        subcommands[4][1].append('')
        subcommands[4][1].append('')

        # get_known_data
        subcommands[5][1].append('')
        subcommands[5][1].append('')
        subcommands[5][1].append('')
        subcommands[5][1].append(subcommands[7][1][4])
        subcommands[5][1].append(subcommands[7][1][5])

        # filter_vcfs
        subcommands[6][1].append('')
        subcommands[6][1].append(subcommands[7][1][1])
        subcommands[6][1].append('')

        subcommands[6][1].clear()

    for multiplicity in Counter([pair[0] for pair in subcommands]).values():
        if multiplicity != 1:
            print("Please only call a function_called once.")
            return 5

    print(subcommands)

    # # Consult with required args checklist
    count = 0
    for i in range(len(subcommands)):
        function_called = subcommands[i][0]
        args = subcommands[i][1]
        for j in range(len(args)):
            if args[j] == '' or args[j] == {}:
                if i == 0 and j == 0:
                    # no original input file was provided
                    print("Error: no original input file was specified.")
                    return 6
                if j == 0:
                    if function_called == "get_vcfs" or function_called == "filter_vcfs":
                        if len(subcommands[i - 2][1]) == 0:
                            print("Error: no original input file was specified.")
                            return 6.25
                    else:
                        if i != 0 and len(subcommands[i - 1][1]) == 0:
                            print("Error: no original input file was specified.")
                            return 6.375
                    if function_called == "get_vcfs" or function_called == "filter_vcfs":
                        args[j] = "%s" % (subcommands[i - 2][1][1])
                    else:
                        args[j] = "%s" % (subcommands[i - 1][1][1])
                    print("No input file was specified for %s. Using %s." % (function_called, args[j]))
                if j == 1:
                    # no output was provided - create output file based on input parameters
                    if function_called != "get_depth" and (os.path.isdir(args[0]) or function_called == "get_known_data"):
                        containing_folder = subcommands[i][1][0][:subcommands[i][1][0].rfind('/') + 1][
                                            :subcommands[i][1][0].rfind('/') + 1]
                        if function_called == "merge_bams":
                            args[j] = "%smerged_bams" % containing_folder
                        elif function_called == "get_vcfs":
                            args[j] = "%svcfs" % containing_folder
                        elif function_called == "remove_chr00":
                            args[j] = "%sno00_vcfs" % containing_folder
                        elif function_called == "unknown_N_filter":
                            args[j] = "%sN_filtered_vcfs" % containing_folder
                        elif function_called == "get_known_data":
                            args[j] = "%sknown_calls" % containing_folder
                        elif function_called == "filter_vcfs":
                            args[j] = "%sfiltered_vcfs" % containing_folder

                    else:
                        if function_called == "merge_bams":
                            print("Error: merged_bams must take a directory.")
                            print('|' + args[0] + '|')
                            return 6.5
                        if function_called == "get_vcfs":
                            args[j] = "%s.vcf" % (subcommands[i][1][0])
                        elif function_called == "remove_chr00":
                            args[j] = "%s_no00.vcf" % (subcommands[i][1][0][:-4])
                        elif function_called == "unknown_N_filter":
                            args[j] = "%sno_high_Ns.vcf" % (subcommands[i][1][0][:-4])
                        elif function_called == "get_depth":
                            args[j] = "%s%s_depth_file.txt" % (subcommands[i][1][0][:subcommands[i][1][0].rfind('/') + 1][
                                            :subcommands[i][1][0].rfind('/') + 1], subcommands[i][1][0][subcommands[i][1][0].rfind('/') + 1:])
                        elif function_called == "filter_vcfs":
                            args[j] = "%s_filtered.vcf" % (subcommands[i][1][0][:-4])
                    print("No output file was specified for %s. Writing to %s." % (function_called, args[j]))
                if j == 2 and function_called == "unknown_N_filter":
                    #no reference file was provided
                    print("Error: to run unknown_N_filter, you must take a reference file.")
                    return 6.5
                if j == 3:
                    # MUST ADD A DIGIT TO ALL INDEXES BELOW!!
                    # no depth_file was provided
                    if len(subcommands[1][1]) < 2 and (subcommands[i - 1][0] == "unknown_N_filter" or
                           len(subcommands[i - 1][1]) < 3) and \
                           (subcommands[i - 1][0] == "unknown_N_filter" or len(subcommands[i - 2][1]) < 3):
                        print("Error: no original depth_file was specified.")
                        return 7
                    else:
                        if subcommands[i - 1][0] != "unknown_N_filter" and len(subcommands[i - 1][1]) >= 3:
                            args[j] = "%s" % (subcommands[i - 1][1][2])
                        else:
                            args[j] = "%s" % (subcommands[1][1][1])
                        print("No depth file was specified for %s. Using %s" % (function_called, args[j]))
                if j == 4:
                    # no true_positive_file was provided
                    if len(subcommands[i - 1][1]) < 4 and len(subcommands[i - 2][1]) < 4:
                        print("Error: no original true_positive_file was specified.")
                        return 8
                    else:
                        if len(subcommands[i - 2][1]) >= 4:
                            args[j] = "%s" % (subcommands[i - 2][1][3])
                        else:
                            args[j] = "%s" % (subcommands[i - 1][1][3])
                        print("No true_positive_file was specified for %s. Using %s" % (function_called, args[j]))
                if j == 5:
                    # no false_positive_file was provided
                    if len(subcommands[i - 1][1]) < 5 and len(subcommands[i - 2][1]) < 5:
                        print("Error: no original false_positive_file was specified.")
                        return 9
                    else:
                        if len(subcommands[i - 2][1]) >= 5:
                            args[j] = "%s" % (subcommands[i - 2][1][4])
                        else:
                            args[j] = "%s" % (subcommands[i - 1][1][4])
                        print("No false_positive_file was specified for %s. Using %s" % (function_called, args[j]))
        if len(args) >= 2 and os.path.isdir(args[0]) and not os.path.isdir(args[1]) and function_called != \
                "get_depth" and function_called != "all":
            os.makedirs(args[1])

        count += 1

    for pair in subcommands:
        if not len(pair[1]) == 0:
            if pair[0] != "merge_bams" and os.path.isdir(pair[1][0]):
                first = True
                if not os.listdir(pair[1][0]):
                    print("%s was called with an empty directory." % pair[0])
                    return 10
                for file in os.listdir(pair[1][0]):
                    print(file)
                    is_callable = False
                    in_file = pair[1][0] + '/' + file
                    out_file = pair[1][1] + '/' + file
                    if pair[0] == "merge_bams" and file.endswith(".bam"):
                        is_callable = True
                        out_file += "m.bam"
                    elif pair[0] == "get_depth" and file.endswith(".bam"):
                        is_callable = True
                        out_file = pair[1][0][:pair[1][0].rfind('/')]
                        if pair[1][0].endswith('/'):
                            out_file = out_file[:out_file.rfind('/')]
                        out_file += '/' + "%s_depth_file.txt" \
                                   % pair[1][0][pair[1][0].rfind('/') + 1:]
                    elif pair[0] == "get_vcfs" and file.endswith(".bam"):
                        is_callable = True
                        out_file += ".vcf"
                    elif pair[0] == "remove_chr00" and file.endswith(".vcf"):
                        is_callable = True
                        out_file += ".no00.vcf"
                    elif pair[0] == "unknown_N_filter" and file.endswith(".vcf"):
                        is_callable = True
                        out_file += ".no_high_Ns.vcf"
                    elif pair[0] == "get_known_data" and file.endswith(".vcf"):
                        is_callable = True
                        out_file = pair[1][1] + '/'
                    elif pair[0] == "filter_vcfs" and file.endswith(".vcf"):
                        is_callable = True
                        out_file += ".filtered.vcf"
                    if not is_callable:
                        continue
                    parameters = "'%s', '%s', " % (in_file, out_file)
                    for parameter in pair[1][2:]:
                        if isinstance(parameter, dict):
                            parameters += "%s, " % parameter
                        else:
                            if parameter == depth_file:
                                parameters += "%s, " % depth_dict
                            else:
                                parameters += "'%s', " % parameter
                    if pair[0] == "get_depth" or pair[0] == "get_known_data":
                        parameters += "%s" % first
                    else:
                        parameters = parameters[:-2]

                    print("Calling %s" % pair[0])
                    print(parameters)

                    function_called_return_value = eval("%s.%s(%s)" % (pair[0], pair[0], parameters))
                    if function_called_return_value != 0:
                        return function_called_return_value
                    first = False
                    is_callable = False

            else:
                parameters = ""
                for parameter in pair[1]:
                        if isinstance(parameter, dict):
                            parameters += "%s, " % parameter
                        else:
                            parameters += "'%s', " % parameter
                if pair[0] == "get_depth" or pair[0] == "get_known_data":
                    parameters += "%s" % True
                else:
                    parameters = parameters[:-2]
                print("Calling %s" % pair[0])

                function_called_return_value = eval("%s.%s(%s)" % (pair[0], pair[0], parameters))
                if function_called_return_value != 0:
                    return function_called_return_value

            if pair[0] == "get_depth":
                depth_file = pair[1][1]
                reading_depth = open(depth_file)
                depth_dict = {}
                line = reading_depth.readline()
                while line:
                    file_depth = line.split(':')
                    depth_dict[file_depth[0]] = float(file_depth[1])
                    line = reading_depth.readline()
                reading_depth.close()

    return 123


# ---
sys.exit(main(sys.argv[1:]))
