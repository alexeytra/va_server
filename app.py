from flask import Flask, jsonify, send_file
from flask import request
from classes.IntentClassifier import IntentClassifier
from classes.Seq2Seq import Seq2SeqModel
from utils.audio_worker import text_to_speech, speech_to_text
from utils.intent_processing import get_answer_from_tag
import os
from utils.load_data import classes, ic_model, ic_tokenizer, label_encoder, seq2seq_model, seq2seq_tokenizer
from yargy import Parser
from yargy.pipelines import morph_pipeline
from datetime import date

app = Flask(__name__)

BASE_URL = '/va/api/v1/'
app.config['UPLOAD_PATH'] = '/temp_data/'

KEY_WORDS = ['Системы информатики', 'СИ',
             'Электротехнический', 'ЭТФ',
             'Строительный', 'СФ', 'Электронно-вычислительные системы',
             'Электронно вычислительные системы', "ЭВС"]
RULE = morph_pipeline(KEY_WORDS)
parser = Parser(RULE)


def process_question(data):
    response = {
        "audioAnswer": request.host_url + BASE_URL[1:] + 'audio_answer'
    }
    question = data['question']
    extract_entity = ''
    if parser.find(question):
        extract_entity = [_.value for _ in parser.find(question).tokens]
        extract_entity = ' '.join(map(str, extract_entity))
        question = question.replace(extract_entity, '').strip()
    intent_classifier = IntentClassifier(classes, ic_model, ic_tokenizer, label_encoder)
    intent_tag = intent_classifier.get_intent(question)
    if intent_tag == 'unrecognized_question':
        seq2seq = Seq2SeqModel(seq2seq_model, seq2seq_tokenizer, 15)
        answer = seq2seq.get_answer(question)
        response['answer'] = answer
        response['seq2seq'] = True
        text_to_speech(answer)
    else:
        data = get_answer_from_tag(intent_tag)
        if data[1] != '':
            answer = str(data[0] + ' ' + data[1])
            text_to_speech(data[0])
            response['answer'] = answer
            response['seq2seq'] = False
            return response
        text_to_speech(data[0])
        response['answer'] = data[0]
        response['seq2seq'] = False
    response['language'] = 'ru'
    response['intent'] = intent_tag
    response['structInfo'] = extract_entity
    response['dateTime'] = date.today()

    return response


@app.route(BASE_URL + 'question/text', methods=['POST'])
def process_question_text():
    data = request.json
    return process_question(data)


@app.route(BASE_URL + 'question/audio', methods=['POST'])
def process_question_audio():
    data = {}
    for f in request.files.getlist('audio'):
        f.save(os.path.join(os.getcwd() + app.config['UPLOAD_PATH'], f.filename))
    data['question'] = speech_to_text("./temp_data/input.wav")
    return process_question(data)


@app.route(BASE_URL + 'audio_answer', methods=['GET'])
def get_audio_answer():
    return send_file('temp_data/outputAudio.mp3')


@app.route(BASE_URL + 'test', methods=['GET'])
def test():
    return os.path.join(os.getcwd() + app.config['UPLOAD_PATH'])


@app.route(BASE_URL + 'test/seq2seq', methods=['POST'])
def test_seq2seq():
    seq2seq = Seq2SeqModel(seq2seq_model, seq2seq_tokenizer, 15)
    return seq2seq.get_answer("Ты милый")


if __name__ == '__main__':
    app.run(debug=True)
