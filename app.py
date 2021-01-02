from flask import Flask, jsonify
from flask import request
from classes.IntentClassifier import IntentClassifier
from utils.AudioWorker import text_to_speech, speech_to_text

# from utils.load_data import classes, model, tokenizer, label_encoder

app = Flask(__name__)


class VAResponse:
    def get(self):
        # intent_classifier = IntentClassifier(classes, model, tokenizer, label_encoder)
        # text_to_speech("Возможно, вы сами знаете, как ответить на этот вопрос")
        print(speech_to_text("./temp_data/input.wav"))
        # return intent_classifier.get_intent("Как у тебя дела")
        return "hello"


@app.route('/')
def hello_world():
    return 'Hello, World!'


# TODO Просто для примера -> потом убрать
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Post'
    else:
        return 'Get'


@app.route("/users")
def users_api():
    users = {
        "users": [
            {"name": "Alex", "age": 22},
            {"name": "Mark", "age": 15},
        ]
    }
    return users


if __name__ == '__main__':
    app.run(debug=True)
