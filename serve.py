from flask import Flask, request
from flask_json import FlaskJSON, JsonError, as_json

import falsefriendsp
from falsefriendsp.falsefriends.classifier import classify
from falsefriendsp.falsefriends import word_vectors, classifier, linear_trans, bilingual_lexicon
from sklearn import svm
from gensim.models import KeyedVectors

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
APP_ROOT = "./"
app.config["APPLICATION_ROOT"] = APP_ROOT
app.config["UPLOAD_FOLDER"] = "files/"

json_app = FlaskJSON(app)

def read_words(file_name):
    with open(file_name) as friends_file:
        friend_pairs = []
        for line in friends_file.readlines():
            word_es, word_pt, true_friends = line.split()
            if true_friends != '-1':
                true_friends = true_friends == '1'
                friend_pairs.append(classifier.FriendPair(word_es, word_pt, true_friends))
    return friend_pairs

#models
training_friend_pairs = read_words(
    "./falsefriendsp/resources/sepulveda2011_training.txt")
model_es = KeyedVectors.load_word2vec_format("./falsefriendsp/resources/big/es.txt")
model_pt = KeyedVectors.load_word2vec_format("./falsefriendsp/resources/big/pt.txt")
T = linear_trans.load_linear_transformation("./falsefriendsp/resources/big/trans_es_300_pt_300.npz")
X_train, y_train = classifier.features_and_labels(training_friend_pairs, model_es, model_pt, T)

@as_json
@app.route("/class_falsefriends", methods=["POST"])
def class_falsefriends():
    data = request.get_json()
    if (data.get('type') != 'structuredText') or ('texts' not in data) or (len(data['texts']) != 2):
        output = invalid_request_error(None)
        return output

    word_es = data["texts"][0]["content"]
    word_pt = data["texts"][1]["content"]
    print(word_pt)
    print(word_es)

    try:
        # Complete here
        output = classify(word_es, word_pt)
        return generate_successful_response(str(output))
    except Exception as e:
        return generate_failure_response(status=404, code="elg.service.internalError", text=None, params=None,
                                         detail=str(e))


@json_app.invalid_json_error
def invalid_request_error(e):
    """Generates a valid ELG "failure" response if the request cannot be parsed"""
    raise JsonError(status_=400, failure={'errors': [
        {'code': 'elg.request.invalid', 'text': 'Invalid request message'}
    ]})


def generate_successful_response(result):
    response = {"type": "classification", "classes": [{"falsefriends": result}]}
    output = {'response': response}
    return output


def generate_failure_response(status, code, text, params, detail):
    error = {}
    if code: error["code"] = code
    if text: error["text"] = text
    if params: error["params"] = params
    if detail: error["detail"] = detail

    raise JsonError(status_=status, failure={'errors': [error]})


def classify(word_es, word_pt):

    # Friends pair constructor
    friends_pair = [
        falsefriendsp.falsefriends.classifier.FriendPair(word_es, word_pt, False)]  # false friends as default

    X_test, y_test = classifier.features_and_labels(friends_pair, model_es, model_pt, T, topx=True)

    clf = classifier.build_classifier(svm.SVC())
    clf.fit(X_train, y_train)

    predicted = clf.predict(X_test)

    return predicted[0]


# def generate_linear_trans(model_es, model_pt):
#     lexicon = bilingual_lexicon.bilingual_lexicon()
#     X, Y = zip(*word_vectors.bilingual_lexicon_vectors(model_es, model_pt, bilingual_lexicon=lexicon))
#     T = linear_trans.linear_transformation(X, Y)
#     linear_trans.save_linear_transformation("./falsefriendsp/resources/big/trans_es_300_pt_300.npz", T)
#
#     return T





if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8866)

