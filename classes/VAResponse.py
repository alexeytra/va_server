from datetime import date

from yargy import Parser
from yargy.pipelines import morph_pipeline

from utils.KEY_WORDS import KEY_WORDS
from utils.audio_worker import text_to_speech
from utils.intent_processing import get_answer_from_tag
from utils.load_data import classes, ic_model, ic_tokenizer, label_encoder, seq2seq_model, seq2seq_tokenizer
from classes.IntentClassifier import IntentClassifier
from classes.Seq2Seq import Seq2SeqModel


class VAResponse:
    def __init__(self, url_audio, question):
        self._url_audio = url_audio
        self._question = question
        self._answer = ''
        self._seq2seq = False
        self._language = 'ru'
        self._intent = ''
        self._struct_info = ''
        self._date_time = ''
        RULE = morph_pipeline(KEY_WORDS)
        parser = Parser(RULE)
        self._parser = parser
        self._process_question()

    def _process_question(self):
        self._extract_info()

        intent_classifier = IntentClassifier(classes, ic_model, ic_tokenizer, label_encoder)
        intent_tag = intent_classifier.get_intent(self._question)

        if intent_tag == 'unrecognized_question':
            seq2seq = Seq2SeqModel(seq2seq_model, seq2seq_tokenizer, 15)
            answer = seq2seq.get_answer(self._question)
            self._answer = answer
            self._seq2seq = True
            text_to_speech(answer)
        else:
            data = get_answer_from_tag(intent_tag)
            if data[1] != '':
                answer = str(data[0] + ' ' + data[1])
                text_to_speech(data[0])
                self._answer = answer
                self._seq2seq = False
            else:
                self._answer = data[0]
                text_to_speech(data[0])
            self._seq2seq = False
            self._intent = intent_tag
        self._date_time = date.today()

    def _extract_info(self):
        if self._parser.find(self._question):
            extract_entity = [_.value for _ in self._parser.find(self._question).tokens]
            self._struct_info = ' '.join(map(str, extract_entity))
            self._question = self._question.replace(self._struct_info, '').strip()

    def get_response(self):
        return {
            "audioAnswer": self._url_audio,
            "answer": self._answer,
            "seq2seq": self._seq2seq,
            "language": self._language,
            "intent": self._intent,
            "structInfo": self._struct_info,
            "dataTime": self._date_time
        }
