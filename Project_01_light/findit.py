#!/bin/sh

import re
import glob



def countConstituents(dir_path):
    pattern_s = "\(S\ "
    pattern_np = "\(NP\ "
    pattern_vp = "\(VP\ "
    pattern_dvp = "\(VP\s\w+\s\(NP\b(.*)\)\s\(NP\b(.*)\)\)"  # (VP verb(NP ...) (NP ...))
    pattern_ivp = "\\(VP\s\w+\)"  # (VP verb)

    count_s = 0
    count_np = 0
    count_vp = 0
    count_dvp = 0
    count_ivp = 0

    for i in dir_path.glob('**/*'):
        prd = open(i, "r", encoding='utf-8')
        prd_text = prd.read().replace('\n', '').replace('\t', '')
        count_s += len(re.findall(pattern_s, prd_text))
        count_np += len(re.findall(pattern_np, prd_text))
        count_vp += len(re.findall(pattern_vp, prd_text))
        count_dvp += len(re.findall(pattern_dvp, prd_text))
        count_ivp += len(re.findall(pattern_ivp, prd_text))

    summary_out = {'Sentence': count_s, 'Noun Phrase': count_np, 'Verb Phrase': count_vp,
                   'Ditransitive Verb Phrase': count_dvp, 'Intransitive Verb Phrase': count_ivp}
    for key, value in summary_out.items():
        print(key + "\t" + str(value))