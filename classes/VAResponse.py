from datetime import date

from yargy import Parser
from yargy.pipelines import morph_pipeline

from utils.constants import KEY_WORDS
from utils.audio_worker import text_to_speech
from utils.intent_processing import get_answer_from_tag, load_additional_info
from utils.load_data import classes, ic_model, ic_tokenizer, label_encoder, seq2seq_model, seq2seq_tokenizer
from classes.IntentClassifier import IntentClassifier
from classes.Seq2Seq import Seq2SeqModel


class VAResponse:
    def __init__(self, url_audio, question):
        self.__url_audio = url_audio
        self.__question = question
        self.__answer = ''
        self.__seq2seq = False
        self.__language = 'ru'
        self.__intent = ''
        self.__struct_info = ''
        self.__date_time = ''
        self.__intent_accuracy = 0.0
        RULE = morph_pipeline(KEY_WORDS)
        parser = Parser(RULE)
        self.__parser = parser
        self.__process_question()

    def __process_question(self):
        self.__extract_info()

        intent_classifier = IntentClassifier(classes, ic_model, ic_tokenizer, label_encoder)
        intent_tag = intent_classifier.get_intent(self.__question)
        self.__intent_accuracy = intent_classifier.accuracy
        self.__intent = intent_tag
        if intent_tag == 'unrecognized_question':
            self.__seq2seq_processing()
        else:
            self.__intent_processing()
        self.__date_time = date.today()

    def __extract_info(self):
        if self.__parser.find(self.__question):
            extract_entity = [_.value for _ in self.__parser.find(self.__question).tokens]
            self.__struct_info = ' '.join(map(str, extract_entity))
            self.__question = self.__question.replace(self.__struct_info, '').strip()

    def __process_struct_info(self):
        return load_additional_info(self.__struct_info.lower(), self.__intent)

    def __seq2seq_processing(self):
        seq2seq = Seq2SeqModel(seq2seq_model, seq2seq_tokenizer, 15)
        answer = seq2seq.get_answer(self.__question)
        self.__answer = answer
        self.__seq2seq = True
        text_to_speech(answer)

    def __intent_processing(self):
        data = get_answer_from_tag(self.__intent)
        self.__seq2seq = False
        if data[1] != '':
            answer = str(data[0] + ' ' + data[1])
            text_to_speech(data[0])
            self.__answer = answer
            self.__seq2seq = False
        else:
            self.__answer = data[0]
            text_to_speech(data[0])
            if self.__extract_info() != '':
                self.__answer = self.__answer.replace('*', self.__struct_info)
                self.__answer += ' ' + self.__process_struct_info()

    def get_response(self):
        return {
            "audioAnswer": self.__url_audio,
            "answer": self.__answer,
            "seq2seq": self.__seq2seq,
            "language": self.__language,
            "intent": self.__intent,
            "structInfo": self.__struct_info,
            "dataTime": self.__date_time,
            "accuracy": round(float(self.__intent_accuracy), 3)
        }
