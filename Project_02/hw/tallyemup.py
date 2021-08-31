#!/opt/python-3.6/bin/python3.6

import sys
import re
import os
from collections import Counter


def process_text(doc):
    # remove SGML tags
    doc_clean = doc.replace('\n', ' ').replace('\t', ' ')
    doc_clean = re.sub(r"<[^>]*>", ' ', doc_clean)
    # remove leading and trailing spaces
    doc_clean = doc_clean.strip()
    # segment by whitespace
    doc_token = re.split(r"\s+", doc_clean)
    # remove words using unacceptable characters
    r = re.compile("^(?!')+[a-zA-Z']+(?<!')$")
    doc_filtered = list(filter(r.match, doc_token))
    r_not = re.compile("^((?!'{2,}).)*$")
    doc_filtered = list(filter(r_not.match, doc_filtered))
    doc_filtered = [x.lower() for x in doc_filtered]

    return doc_filtered

    # filter out words that start or end with a straight apostrophe (no within a word)
    # lower case all


def load_files(dir_path):
    file_ls = []
    for i in os.listdir(dir_path):
        f = os.path.join(dir_path, i)
        if os.path.isfile(f):
            prd = open(f, "r", encoding='utf8')
            prd_text = prd.read()
            prd_text = process_text(prd_text)
            file_ls += prd_text

    count_dict = Counter(file_ls)

    for key, value in count_dict.most_common():
        print(key + "\t" + str(value))


load_files(sys.argv[1])
