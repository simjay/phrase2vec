import gensim
import sys
import os


class TextIterator(object):

    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()


def train_model(input_dir_path, output_dir_path):
    sentences = TextIterator(input_dir_path)
    model = gensim.models.Word2Vec(sentences, size=200, workers=1)
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    model.save(os.path.join(output_dir_path, "p2v_model.bin"))


def main():
    input_dir_path = sys.argv[1]
    output_dir_path = sys.argv[2]
    train_model(input_dir_path, output_dir_path)


if __name__ == "__main__":
    main()
