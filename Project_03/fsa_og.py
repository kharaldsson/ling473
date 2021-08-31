#!/opt/python-3.6/bin/python3.6

import sys
import re
import os


def create_cat2chars(input_ls):
    cat_keys = []
    cat_values = []
    for i in input_ls:
        cats_cl = i.replace('\n', '').replace('\t', '')
        cats_split = re.split(r"\s+", cats_cl, maxsplit=1)
        cat_split_vals = re.split(r"\s+", cats_split[1])
        cat_keys.append(cats_split[0])
        cat_values.append(cat_split_vals)

    out_dict = dict(zip(cat_keys, cat_values))

    return out_dict


def process_lines(lines, fsa, cat2chars):
    segmented_ls = []

    for line in lines:
        segmented = ""
        current_state_index = 0
        for char in line:
            for category, to_state_index in fsa[current_state_index]:
                if char in cat2chars[category]:
                    current_state_index = to_state_index
                    break

            if current_state_index == 7 or current_state_index == 8:
                segmented = segmented + " " + char
                current_state_index = fsa[current_state_index]

            elif current_state_index == 9:
                segmented = segmented + char + " "
                current_state_index = fsa[current_state_index]
            else:
                segmented = segmented + char

        segmented = segmented + "\n"

        segmented_ls.append(segmented)

    return segmented_ls


def process_file(category_path, input_path, output_path):
    fsa_dict = {
        0: [('V1', 1), ('C1', 2)]
        , 1: [('C1', 2)]
        , 2: [('C2', 3), ('V2', 4), ('T', 5), ('V3', 6), ('C3', 9), ('V1', 7), ('C1', 8)]
        , 3: [('V2', 4), ('T', 5), ('V3', 6), ('C3', 9)]
        , 4: [('T', 5), ('V3', 6), ('C3', 9), ('V1', 7), ('C1', 8)]
        , 5: [('V3', 6), ('C3', 9), ('V1', 7), ('C1', 8)]
        , 6: [('C3', 9), ('V1', 7), ('C1', 8)]
        , 7: 1
        , 8: 2
        , 9: 0
    }

    # Import Categories
    with open(category_path, 'r', encoding='utf8') as f:
        cats = f.readlines()

    # Import input text
    with open(input_path, 'r', encoding='utf8') as f:
        lines_raw = f.readlines()

    lines_cl = [s.replace('\n', '') for s in lines_raw]
    cats_dict = create_cat2chars(cats)

    segments = process_lines(lines_cl, fsa_dict, cats_dict)

    output_fname = 'output'
    output = os.path.join(output_path, output_fname)
    with open(output, 'w', encoding='utf8') as f:
        f.writelines(segments)


# def run(category_path, input_path, output_path):
#     fsa = {
#         0: [('V1', 1), ('C1', 2)]
#         , 1: [('C1', 2)]
#         , 2: [('C2', 3), ('V2', 4), ('T', 5), ('V3', 6), ('C3', 9), ('V1', 7), ('C1', 8)]
#         , 3: [('V2', 4), ('T', 5), ('V3', 6), ('C3', 9)]
#         , 4: [('T', 5), ('V3', 6), ('C3', 9), ('V1', 7), ('C1', 8)]
#         , 5: [('V3', 6), ('C3', 9), ('V1', 7), ('C1', 8)]
#         , 6: [('C3', 9), ('V1', 7), ('C1', 8)]
#         , 7: 1
#         , 8: 2
#         , 9: 0
#     }
#
#     # Import Categories
#     with open(category_path, 'r', encoding='utf8') as f:
#         cats = f.readlines()
#
#     # Import input text
#     with open(input_path, 'r', encoding='utf8') as f:
#         lines_raw = f.readlines()
#
#     lines_cl = [s.replace('\n', '') for s in lines_raw]
#     cat2chars = create_cat2chars(cats)
#
#     segmented_ls = []
#     segmented_str = ""
#
#     for line in lines_cl:
#         segmented = ""
#         current_state_index = 0
#         for char in line:
#             for category, to_state_index in fsa[current_state_index]:
#                 if char in cat2chars[category]:
#                     current_state_index = to_state_index
#                     break
#
#             if current_state_index == 7 or current_state_index == 8:
#                 segmented = segmented + " " + char
#                 current_state_index = fsa[current_state_index]
#
#             elif current_state_index == 9:
#                 segmented = segmented + char + " "
#                 current_state_index = fsa[current_state_index]
#             else:
#                 segmented = segmented + char
#         segmented = segmented + "\n"
#         segmented_ls.append(segmented)
#         segmented_str = segmented_str + segmented
#
#     output_fname = 'output'
#     output = os.path.join(output_path, output_fname)
#     with open(output, 'w', encoding='utf8') as f:
#         f.writelines(segmented_ls)


category_file = "/Users/Karl/LING473/Projects/Project_03/project3/category.txt"
input_file = "/Users/Karl/LING473/Projects/Project_03/project3/input.txt"
output_file = "/Users/Karl/LING473/Projects/Project_03/data_processed"

process_lines(category_file, input_file, output_file)
# load_files(sys.argv[1])
