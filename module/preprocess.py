from nltk.tokenize import sent_tokenize, word_tokenize
from unidecode import unidecode
import string
import spacy
import sys
import os
import re


nlp = spacy.load('en')

articles = ['a', 'an', 'the']


def sentence_tokenize(string):
    """
    Tokenize a chunk of text into sentence tokens.
    In this method, non-unicode characters will be substituted by similar unicode characters.
    params:
        string (str): a chunk of text in raw format.
    return:
        (list) a list of sentence tokens.
    """
    string = string.replace('-\r', '').replace('\r', ' ')
    string = string.replace('-\n', '').replace('\n', ' ')
    string = ''.join([i if ord(i) < 128 else unidecode(i) for i in string])
    string = string.lower()
    string = re.sub(' +', ' ', string)
    return sent_tokenize(string)


def phrase_to_key(phrase):
    word_list = [word for word in phrase.split(" ") if word not in articles]
    return "_".join(word_list)


def preprocess_directory(input_dir_path, output_dir_path):
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    for filename in os.listdir(input_dir_path):
        preprocess_file(os.path.join(input_dir_path, filename), os.path.join(output_dir_path, filename))


def preprocess_file(input_file_path, output_file_path):
    with open(input_file_path,'r') as r_file:
        with open(output_file_path, 'w') as w_file:
            content = r_file.read()
            for sentence in sentence_tokenize(content):
                modified_sentence = sentence[:]
                doc = nlp(unicode(sentence))
                for chunk in doc.noun_chunks:
                    modified_sentence = modified_sentence.replace(chunk.text,
                                        phrase_to_key(chunk.text), 1)
                w_file.write(modified_sentence + "\n")

# TODO: stem all words except keywords

def main():
    input_dir_path = sys.argv[1]
    output_dir_path = sys.argv[2]
    preprocess_directory(input_dir_path, output_dir_path)


if __name__ == "__main__":
    main()
