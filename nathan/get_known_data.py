import os
from string import ascii_letters
from string import digits
from sys import exit

def get_known_data(input_vcf, output, depth_dict, true_positive_dict, false_positive_dict, overwrite):
    """
    Generates two files: one containing all of lumpy's true positive calls, the other containing all of lumpy's
    false positive calls.
    Usage: get_distribution(input_vcf)
    :param: input_vcf - the file to search for known true and false calls in.
    :param: output - the directory path where both of the output files should be stored.
    :param: depth_dict - the dictionary containing the average read depth of all the BAM files. The dictionary is
    constructed in the following format:
    depth_dict = {
        <file name>.bam:<read depth>,
        <file name>.bam:<read depth>,
        <file name>.bam:<read depth>
        }
    :param: true_positive_dict - A dictionary containing information on all known structural variants. It is in the
    following format:
    true_positive_dict = {
        <chromosome #>.<position in chromosome>:[<chromosome #>.<position in chromosome>, <SV type>]
        <chromosome #>.<position in chromosome>:[<chromosome #>.<position in chromosome>, <SV type>, <SV type>]
        <chromosome #>.<position in chromosome>:[<chromosome #>.<position in chromosome>, <SV type>]
        }
        Please note that you can append as may SV types as desired (this is to account for complex events).
    :param: false_positive_dict - A dictionary containing information on all structural variants calls known to be
    false. It is in the following format:
    false_positive_dict = {
        <chromosome #>.<position in chromosome>:[<chromosome #>.<position in chromosome>, <SV type>]
        <chromosome #>.<position in chromosome>:[<chromosome #>.<position in chromosome>, <SV type>, <SV type>]
        <chromosome #>.<position in chromosome>:[<chromosome #>.<position in chromosome>, <SV type>]
        }
        Please note that you can append as may SV types as desired (this is to account for complex events).
    :param: overwrite - A bool value designed to indicate whether the current true and false positive files should
    be overwritten (True) or appended to (False).
    :return: Number indicating whether get_vcfs was run successfully.
        0 - ran successfully
    """
    if not os.path.exists(output + "true_positives.txt"):
        open(output + "true_positives.txt", 'w').close()
    if not os.path.exists(output + "false_positives.txt"):
        open(output + "false_positives.txt", 'w').close()

    if not isinstance(input_vcf, str) or \
        input_vcf == '' or \
        not input_vcf.endswith(".vcf") or \
        not os.path.isfile(input_vcf) or \
        not os.access(input_vcf, os.R_OK) or \
        not isinstance(output, str) or \
        output == '' or \
        output.rfind('/') == -1 or \
        not os.path.isdir(output[:output.rfind('/') + 1]) or \
        not os.access(output + "true_positives.txt", os.W_OK) or \
        not os.access(output + "false_positives.txt", os.W_OK):
        print("Invalid Input or Output path supplied. The input file itself must exist and be readable and end with"
              ".vcf. While the output must be an existing file directory, and its name may not be "
              "empty and may only contain ASCII characters, numbers, ., -, and _. Moreover, the intended directory"
              "is to be populated with a file called true_positives.txt and false_positives.txt. If these files "
              "already exist, they must be writable.")
        exit()
        return
    elif not isinstance(depth_dict, dict) or \
        not isinstance(true_positive_dict, dict) or \
        not isinstance(false_positive_dict, dict) or \
        not depth_dict or \
        not true_positive_dict or \
        not false_positive_dict:
        print("depth_dict, true_positive_dict, false_positive_dict must all be nonempty dictionaries.")
        exit()
        return
    elif not isinstance(overwrite, bool):
        print("overwrite must have a bool value.")
        exit()
        return

    if overwrite:
        print('overwriting')
        true_positive_file = open(output + "true_positives.txt", 'w')
        false_positive_file = open(output + "false_positives.txt", 'w')
        true_positive_file.write(
            "file\tread depth\tactual type\tcall type\tvalidated pos\tvalidated end\tpredicted pos (95% CI)\tpredicted "
            "end (95% CI)\ttotal evidence\tPE evidence\t SR evidence\t PE:SR ratio\t Imprecise?\n")
        false_positive_file.write(
            "file\tread depth\tactual type\tcall type\tvalidated pos\tvalidated end\tpredicted pos (95% CI)\tpredicted "
            "end (95% CI)\ttotal evidence\tPE evidence\t SR evidence\t PE:SR ratio\t Imprecise?\n")
    else:
        true_positive_file = open(output + "true_positives.txt", 'a')
        false_positive_file = open(output + "false_positives.txt", 'a')


    if input_vcf.endswith(".vcf"):
        print("Getting evidence from " + input_vcf[input_vcf.rfind('/') + 1:])
        reading_vcf = open(input_vcf)
        count_tp = 0
        count_fp = 0
        for line in reading_vcf:
            if line[0] != '#':
                sample = line.split('\t')
                ci_list = (sample[7][sample[7].find("CIPOS95="):sample[7].find(";SU=")]).split(';')
                ci_pos_start = int(ci_list[0][8:ci_list[0].find(',')])
                ci_pos_end = int(ci_list[0][ci_list[0].find(',') + 1:]) + 1
                ci_end_start = int(ci_list[1][8:ci_list[1].find(','):])
                ci_end_end = int(ci_list[1][ci_list[1].find(',') + 1:]) + 1
                is_true_positive = False
                is_false_positive = False
                if sample[4] != "<DEL>" and sample[4] != "<DUP>" and sample[4] != "<INV>" and sample[4] != "<INS>" and \
                        sample[4] != "<CNV>":
                    sv_type = "<BND>"
                else:
                    sv_type = sample[4]
                for position in true_positive_dict.keys():
                    chrom = position[:position.find('.')]
                    pos = int(position[position.find('.') + 1:])
                    if sample[7].find(";END=") != -1:
                        end_pos = sample[7][sample[7].find(";END=") + 5:sample[7].find(";CIPOS=")]
                        if sample[0].find(chrom) != -1 and \
                                pos in range(int(sample[1]) + ci_pos_start, int(sample[1]) + ci_pos_end) and \
                                int(true_positive_dict[position][0][true_positive_dict[position][0].find('.') + 1:]) \
                                in range(int(end_pos) + ci_end_start, int(end_pos) + ci_end_end) and \
                                sv_type in true_positive_dict[position][1]:
                            # SV Call is true_positive_dict
                            print("\tFound True Pos:\t%s\t%s\t%s\t%s\t\n" % (
                                pos, (int(sample[1]) + ci_pos_start, int(sample[1]) + ci_pos_end),
                                true_positive_dict[position][0][true_positive_dict[position][0].find('.') + 1:],
                                (int(end_pos) + ci_end_start, int(end_pos) + ci_end_end)))
                            count_tp += 1
                            is_true_positive = True
                            key_pos = position
                            alt_pos = sample[1]
                            pos_ci = (int(sample[1]) + ci_pos_start, int(sample[1]) + ci_pos_end)
                            key_end = true_positive_dict[position][0]
                            alt_end = end_pos
                            end_ci = (int(end_pos) + ci_end_start, int(end_pos) + ci_end_end)
                            actual_sv_type = true_positive_dict[position][1][:-1]
                            if sample[7].find('IMPRECISE') != -1:
                                imprecise = 'Y'
                            else:
                                imprecise = 'N'
                            break
                        else:
                            # SV Call untrue_positive_dict
                            pass
                    # elif sample[0].find(chrom) != -1 and \
                    #         pos in range(int(sample[1]) + ci_pos_start, int(sample[1]) + ci_pos_end):
                    #     # breakend called at start of SV
                    #     print("\tFound True Pos:\t%s\t%s\t%s\t%s\n" % (
                    #         pos, (int(sample[1]) + ci_pos_start, int(sample[1]) + ci_pos_end), sv_type,
                    #         true_positive_dict[position][1]))
                    #     count_tp += 1
                    #     is_true_positive = True
                    #     key_pos = position
                    #     alt_pos = sample[1]
                    #     pos_ci = (int(sample[1]) + ci_pos_start, int(sample[1]) + ci_pos_end)
                    #     key_end = true_positive_dict[position][0]
                    #     alt_end = ""
                    #     end_ci = ""
                    #     actual_sv_type = true_positive_dict[position][1][:-1]
                    #     if sample[7].find('IMPRECISE') == -1:
                    #         imprecise = 'N'
                    #     else:
                    #         imprecise = 'Y'
                    #     break
                    else:
                        # breakend untrue_positive_dict
                        pass
                if not is_true_positive:
                    for position in false_positive_dict.keys():
                        chrom = position[:position.find('.')]
                        pos = int(position[position.find('.') + 1:])
                        if sample[7].find(";END=") != -1:
                            end_pos = sample[7][sample[7].find(";END=") + 5:sample[7].find(";CIPOS=")]
                            if sample[0].find(chrom) != -1 and \
                                    pos in range(int(sample[1]) + ci_pos_start, int(sample[1]) + ci_pos_end) and \
                                    int(false_positive_dict[position][0][
                                        false_positive_dict[position][0].find('.') + 1:]) in \
                                    range(int(end_pos) + ci_end_start, int(end_pos) + ci_end_end) and \
                                    sv_type in false_positive_dict[position][1]:
                                # SV Call is false positive
                                print("\tFound False Pos:\t%s\t%s\t%s\t%s\n" % (
                                    false_positive_dict[position][0][false_positive_dict[position][0].find('.') + 1:],
                                    (int(end_pos) + ci_end_start, int(end_pos) + ci_end_end), sv_type,
                                    false_positive_dict[position][1]))
                                count_fp += 1
                                is_false_positive = True
                                key_pos = position
                                alt_pos = sample[1]
                                pos_ci = (int(sample[1]) + ci_pos_start, int(sample[1]) + ci_pos_end)
                                key_end = false_positive_dict[position][0]
                                alt_end = end_pos
                                end_ci = (int(end_pos) + ci_end_start, int(end_pos) + ci_end_end)
                                actual_sv_type = false_positive_dict[position][1]
                                if sample[7].find('IMPRECISE') == -1:
                                    imprecise = 'N'
                                else:
                                    imprecise = 'Y'
                                break
                            else:
                                # SV Call untrue_positive_dict
                                pass
                        else:
                            # breakend untrue_positive_dict
                            pass

                # write calls of interest to pertinent file
                read_depth = depth_dict[input_vcf[input_vcf.rfind('/') + 1:input_vcf.find(".bam") + 4]]
                su = sample[9][:-1].split(':')[1]
                pe = sample[9][:-1].split(':')[2]
                sr = sample[9][:-1].split(':')[3]
                if is_true_positive:
                    true_positive_file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s %s\t%s %s\t%s\t%s\t%s\t%s\t%s\n" % (
                        input_vcf[input_vcf.rfind('/') + 1:], read_depth, actual_sv_type, sv_type, key_pos, key_end,
                        alt_pos, pos_ci, alt_end, end_ci, su, pe, sr, float(sr) / float(pe), imprecise))
                elif is_false_positive:
                    false_positive_file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s %s\t%s %s\t%s\t%s\t%s\t%s\t%s\n" % (
                        input_vcf[input_vcf.rfind('/') + 1:], read_depth, actual_sv_type, sv_type, key_pos, key_end,
                        alt_pos, pos_ci, alt_end, end_ci, su, pe, sr, float(sr) / float(pe), imprecise))

        print("Found %d true positives and %d false positives." % (count_tp, count_fp))

    reading_vcf.close()
    true_positive_file.close()
    false_positive_file.close()


    return 0
