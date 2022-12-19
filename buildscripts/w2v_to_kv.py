from gensim.models import KeyedVectors
import sys

model = KeyedVectors.load_word2vec_format(sys.argv[1])
model.save(sys.argv[2])
