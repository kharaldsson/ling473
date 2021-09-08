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
        # self.lines = lines

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


class NaiveBayes:
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


def run(model_path, input_file_path, output_file):



# process_files(sys.argv[1], sys.argv[2])
test_file = "/Users/Karl/LING473/Projects/Project_05/project5/language_models/dan.unigram-lm"
test_path = "/Users/Karl/LING473/Projects/Project_05/project5/language_models"
test_sentence = "Matatagpuan sa kalagitnaan ng Hilagang Amerika ang karamihan sa mga estado nito kung saan mayroong sariling pamahalaan ang bawat isa na naaayon sa sistemang pederalismo"
# test_sentence = "Jeg håber at medlemmerne vil gøre de kolleger som måske går rundt udenfor og leder efter den opmærksom på dette"
# test_lang = Language(test_file)
# # out = test_lang.load_data()
# print(test_lang.probabilities_dictionary)
# # print(test_lang.build_model())
# print(test_lang.get_probability("for"))
# print(test_lang.name)

test_model = NaiveBayes(test_path)
test_model.predict_log_proba(test_sentence)
print(test_model.probabilities)
print(test_model.result)
