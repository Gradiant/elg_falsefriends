from flask import Flask, request
from flask_json import FlaskJSON, JsonError, as_json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
APP_ROOT = "./"
app.config["APPLICATION_ROOT"] = APP_ROOT
app.config["UPLOAD_FOLDER"] = "files/"

json_app = FlaskJSON(app)

@as_json
@app.route("/predict_json", methods=["POST"])
def predict_json():

    data = request.get_json()
    if (data.get('type') != 'text') or ('content' not in data):
        output = invalid_request_error(None)
        return output

    content = data["content"]

    try:
        # Complete here
        output = None
        return output
    except Exception as e:
        return generate_failure_response(status=404, code="elg.service.internalError", text=None, params=None,
                                         detail=e)


@json_app.invalid_json_error
def invalid_request_error(e):
    """Generates a valid ELG "failure" response if the request cannot be parsed"""
    raise JsonError(status_=400, failure={'errors': [
        {'code': 'elg.request.invalid', 'text': 'Invalid request message'}
    ]})


def generate_successful_response(text, language):
    response = {"type": "classification", "classes": [{"class": language}]}
    output = {'response': response}
    return output


def generate_failure_response(status, code, text, params, detail):
    error = {}
    if code: error["code"] = code
    if text: error["text"] = text
    if params: error["params"] = params
    if detail: error["detail"] = detail

    raise JsonError(status_=status, failure={'errors': [error]})
    # return {"status": status, "failure": {'errors': [error]}}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8866)
