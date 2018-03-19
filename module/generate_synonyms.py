import gensim
import sys


def load_model(model_path):
    global model
    model = gensim.models.Word2Vec.load(model_path)


def generate_synonyms(phrase):
    try:
        return model.most_similar(positive=[phrase.lower()])
    except KeyError:
        return []


def main():
    model_path = sys.argv[1]
    load_model(model_path)

if __name__ == "__main__":
    main()
