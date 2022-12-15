from gensim.models import KeyedVectors
from falsefriendsp.falsefriends import word_vectors, linear_trans, bilingual_lexicon, classifier
import numpy as np
import sys


def read_words(file_name):
    with open(file_name) as friends_file:
        friend_pairs = []
        for line in friends_file.readlines():
            word_es, word_pt, true_friends = line.split()
            if true_friends != '-1':
                true_friends = true_friends == '1'
                friend_pairs.append(classifier.FriendPair(word_es, word_pt, true_friends))
    return friend_pairs


model_es = KeyedVectors.load(sys.argv[1])
model_pt = KeyedVectors.load(sys.argv[2])

lexicon = bilingual_lexicon.bilingual_lexicon()
X, Y = zip(*word_vectors.bilingual_lexicon_vectors(model_es, model_pt, bilingual_lexicon=lexicon))
T = linear_trans.linear_transformation(X, Y)
linear_trans.save_linear_transformation(sys.argv[3], T)

training_friend_pairs = read_words(
    "./falsefriendsp/resources/sepulveda2011_training.txt")

X_train, y_train = classifier.features_and_labels(training_friend_pairs, model_es, model_pt, T)
np.savez(sys.argv[4], X_train=X_train, y_train=y_train)
