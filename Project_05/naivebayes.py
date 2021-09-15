#!/opt/python-3.6/bin/python3.6

import sys
import re
import os
import glob
import math


class Language:
    def __init__(self, filepath):
        self.filepath = filepath
        self.name = os.path.basename(filepath).split('.')[0]
        self.unigram_dictionary = None
        self.num_words = None
        self.probabilities_dictionary = None
        self.build_language()

    def build_language(self):
        with open(self.filepath, 'r', encoding='utf8') as f:
            lines = f.readlines()
        lines = [sub.replace('\n', '') for sub in lines]

        # Split Language Model into Dict
        unigram_keys = []
        unigram_values = []
        for i in lines:
            line_split = re.split(r"\t+", i, maxsplit=1)
            unigram_keys.append(line_split[0])
            unigram_values.append(int(line_split[1]))
        self.unigram_dictionary = dict(zip(unigram_keys, unigram_values))

        # Get Total Number of Words in Language
        self.num_words = sum(self.unigram_dictionary.values())

        # Get probability of each word in language
        self.probabilities_dictionary = {k: v / self.num_words for k, v in self.unigram_dictionary.items()}

        return self.probabilities_dictionary

    def get_probability(self, word):
        return self.probabilities_dictionary[word]


class NaiveBayes(object):
    def __init__(self, language_models_path):
        self.language_models_path = language_models_path
        self.input_sentence = None
        self.unigram_models = []
        self.probabilities = {}
        self.result = None
        self.build_unigram_models()

    def build_unigram_models(self):
        input_files = glob.glob(self.language_models_path + '**/*')
        for file in input_files:
            self.unigram_models.append(Language(file))

    def predict_log_proba(self, input_sentence):
        sentence_tokens = re.split(r"\s+", input_sentence)
        for model in self.unigram_models:
            model_probabilities = []
            for word in sentence_tokens:
                if word in model.probabilities_dictionary:
                    log_prob = math.log(model.get_probability(word), 10)
                    model_probabilities.append(log_prob)
                else:
                    log_prob = math.log(model.get_probability("<UNK>"), 10)
                    model_probabilities.append(log_prob)
            sum_prob = sum(model_probabilities)
            self.probabilities[model.name] = sum_prob
        self.result = max(self.probabilities, key=self.probabilities.get)


def parse_inputs(input_lines):
    out_dict = {}
    for i in input_lines:
        line_clean = i.replace('\n', '')
        line_split = re.split(r"\t+", line_clean, maxsplit=1)
        out_dict[line_split[0]] = line_split[1]

    return out_dict


def run(model_path, input_file_path, output_path):
    nb_model = NaiveBayes(model_path)

    with open(input_file_path, 'r', encoding='utf8') as f:
        inputs = f.readlines()

    sentences = parse_inputs(inputs)

    pred = []
    for key, value in sentences.items():
        nb_model.predict_log_proba(value)
        model_input = key + "\t" + value
        pred.append(model_input)
        for k, v in nb_model.probabilities.items():
            model_prob = k + "\t" + str(v)
            pred.append(model_prob)
        model_result = "result\t" + nb_model.result + "\n"
        pred.append(model_result)

    with open(output_path, 'w', encoding='utf8') as f:
        f.writelines("%s\n" % line for line in pred)


run(sys.argv[1], sys.argv[2], sys.argv[3])