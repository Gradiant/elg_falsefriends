from flask import Flask, request
from flask_json import FlaskJSON, JsonError, as_json

import falsefriendsp
import numpy as np
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


# models
print("Reading Spanish model")
model_es = KeyedVectors.load("./falsefriendsp/resources/big/es.kv")
print("Reading Portuguese model")
model_pt = KeyedVectors.load("./falsefriendsp/resources/big/pt.kv")
print("Loading linear transform")
T = linear_trans.load_linear_transformation("./falsefriendsp/resources/big/trans_es_300_pt_300.npz")
print("Loading training pairs")
with np.load("./falsefriendsp/resources/big/training_pairs.npz") as train_pairs:
    X_train = train_pairs['X_train']
    y_train = train_pairs['y_train']



@as_json
@app.route("/class_falsefriends", methods=["POST"])
def class_falsefriends():
    data = request.get_json()
    if (data.get('type') != 'structuredText') or ('texts' not in data) or (len(data['texts']) != 2):
        output = invalid_request_error(None)
        return output

    word_es = data["texts"][0]["content"]
    word_pt = data["texts"][1]["content"]

    try:
        # Complete here
        output = classify(word_es, word_pt)
        return generate_successful_response(output)
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
    if result:
        result = "false friends"
    else:
        result = "no false friends"
    response = {"type": "classification", "classes": [{"class": result}]}
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8866)
