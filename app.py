from flask import Flask
from classes.IntentClassifier import IntentClassifier
from utils.load_data import classes, model, tokenizer, label_encoder

app = Flask(__name__)


@app.route('/')
def hello_world():
    intent_classifier = IntentClassifier(classes, model, tokenizer, label_encoder)
    return intent_classifier.get_intent("Скажи где ВСГУТУ")


if __name__ == '__main__':
    app.run()
