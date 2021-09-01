#!/opt/python-3.6/bin/python3.6

import sys
import re
import os
import glob


class Node:
    def __init__(self):
        self.children = {'A': None, 'C': None, 'G': None, 'T': None}
        self.end = False
        self.target = None

    def set_target(self, target):
        self.target = target

    def set_child(self, input_char):
        self.children[input_char] = Node()

    def child(self, letter):
        return self.children[letter]


class Trie:
    def __init__(self):
        self.root = Node()

    def build_trie(self, words):
        for word in words:
            self.insert(word)

    def insert(self, word):
        node = self.root
        for char in word:
            if node.children[char] is None:
                node.set_child(char)
            node = node.children[char]
        node.end = True
        node.set_target(word)

    def word_search(self, word):
        node = self.root
        for char in word:
            if char in word:
                if char in node.children:
                    node = node.children[char]
            else:
                return False
        return node.end

    def search(self, input, input_file_name):
        trie_root = self.root
        i = 0
        while i < len(input):
            current_node = trie_root
            j = i
            while current_node is not None and j < len(input):
                letter = input[j].upper()
                if letter == "N":
                    break
                current_node = current_node.children[letter]
                if current_node is None:
                    break
                if current_node.end is True:
                    print(input_file_name + "\t" + str(i) + "\t" + current_node.target)
                    break
                j += 1
            i += 1


def process_files(target_path, input_path):
    # Import Target Sequences
    with open(target_path, 'r', encoding='utf8') as f:
        target_sequences = f.readlines()

    target_sequences = [sub.replace('\n', '') for sub in target_sequences]

    # Build Trie
    trie = Trie()
    trie.build_trie(target_sequences)

    # Import Input data
    input_files = glob.glob(input_path + '**/*')
    for file in input_files:
        text = open(file, "r", encoding='utf-8')
        text_clean = text.read().replace('\n', '').replace('\t', '')
        input_file_name = os.path.basename(file)
        new_trie = trie
        new_trie.search(text_clean, input_file_name)


process_files(sys.argv[1], sys.argv[2])

