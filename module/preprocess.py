from nltk.tokenize import sent_tokenize, word_tokenize
from unidecode import unidecode
import string
import spacy
import sys
import os
import re

nlp = spacy.load('en')

def sentence_tokenize(string):
    """
    Tokenize a chunk of text into sentence tokens.
    In this method, non-unicode characters will be substituted by similar unicode characters.
    params:
        string (str): a chunk of text in raw format.
    return:
        (list) a list of sentence tokens.
    """
    string = string.replace('-\r', '-').replace('\r', ' ')
    string = string.replace('-\n', '-').replace('\n', ' ')
    string = ''.join([i if ord(i) < 128 else unidecode(i) for i in string])
    string = re.sub(' +', ' ', string)
    return sent_tokenize(string)

def preprocess_directory(input_dir_path, output_dir_path):
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    for filename in os.listdir(input_dir_path):
        preprocess_file(os.path.join(input_dir_path, filename), os.path.join(output_dir_path, filename))

def preprocess_file(input_file_path, output_file_path):
    with open(input_file_path,'r') as f:
        content = f.read()
        print(content)
        print("---------")
        # words = [word_tokenize(sent) for sent in sentence_tokenize(content)]
        for sentence in sentence_tokenize(content):
            modified_sentence = sentence[:]
            doc = nlp(unicode(sentence))
            for chunk in doc.noun_chunks:
                #     # print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)
                # print "%s|NOUN" % (chunk.text)
                modified_sentence = modified_sentence.replace(chunk.text, chunk.text.replace(" ", "_"), 1)
            print(modified_sentence)
        # for token in doc:
            # print(token.text, token.dep_, token.head.text, token.head.pos_,
                  # [child for child in token.children])




def main():
    input_dir_path = sys.argv[1]
    output_dir_path = sys.argv[2]
    preprocess_directory(input_dir_path, output_dir_path)

    # doc = nlp(u'Autonomous cars shift insurance liability toward manufacturers')
    # for chunk in doc.noun_chunks:
    #     # print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)
    #     print "%s|%s" % (chunk.text, chunk.root.head.pos)
    # for token in doc:
    #     print(token.text, token.dep_, token.head.text, token.head.pos_, [child for child in token.children])
    # span = doc[doc[4].left_edge.i : doc[4].right_edge.i+1]
    # span.merge()
    # for token in doc:
    #     print(token.text, token.pos_, token.dep_, token.head.text)

if __name__ == "__main__":
    main()
