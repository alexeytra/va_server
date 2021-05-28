from datetime import datetime
from flask import request

from utils.user import *
from constants.constants import BASE_URL, ANSWERS_FOR_UNRECOGNIZED_QUESTIONS, ANSWERS_FOR_WRONG_ANSWERS, \
    ANSWERS_FOR_GOOD_RESPONSE, GREETING_RESPONSE, LOGIN_USER_RESPONSE, LOGOUT_USER_RESPONSE
from utils.audio_worker import text_to_speech
from utils.intent_processing import get_answer_from_tag, load_additional_info
from utils.load_data import classes, ic_model, ic_tokenizer, label_encoder, seq2seq_model, seq2seq_tokenizer, max_len
from classes.IntentClassifier import IntentClassifier
from classes.Seq2Seq import Seq2SeqModel
from classes.EntityExtractor import EntityExtractor
import random


class DialogManager:
    def __init__(self, voice=False, answer_generating=False):
        if voice:
            self.__url_audio = request.host_url + BASE_URL[1:] + 'answer/audio'
        else:
            self.__url_audio = ''
        self.__question = ''
        self.__voice = voice
        self.__answer_generating = answer_generating
        self.__answer = ''
        self.__seq2seq = False
        self.__language = 'ru'
        self.__intent = ''
        self.__struct_info = ''
        self.__entity = {}
        self.__intent_accuracy = 0.0
        self.__options_for_questions = []
        self.__additional_response = ""

    def __extract_info(self):
        entity_extractor = EntityExtractor()
        self.__entity = entity_extractor.extract_entity(self.__question)
        if self.__entity:
            self.__struct_info = self.__entity['entity']
            self.__question = self.__question.replace(self.__struct_info, '').strip()
        else:
            self.__struct_info = ''

    def process_question(self, question):
        self.__question = question
        if self.__question == '👍':
            self.__process_good_response()
            return
        self.__extract_info()

        intent_classifier = IntentClassifier(classes, ic_model, ic_tokenizer, label_encoder, max_len)
        intent_tag = intent_classifier.get_intent(self.__question)
        self.__intent_accuracy = intent_classifier.accuracy
        self.__intent = intent_tag

        if intent_tag == 'unrecognized_question' and self.__answer_generating:
            self.__seq2seq_processing()
        elif intent_tag == 'unrecognized_question' and not self.__answer_generating:
            self.__answer = random.choice(ANSWERS_FOR_UNRECOGNIZED_QUESTIONS)
            if self.__voice:
                text_to_speech(self.__answer)
        else:
            self.__intent_processing()

    def process_wrong_answer(self, data):
        self.__answer = random.choice(ANSWERS_FOR_WRONG_ANSWERS)
        if self.__voice:
            text_to_speech(self.__answer)

    def __process_struct_info(self):
        return load_additional_info(self.__entity['key'], self.__intent)

    def __seq2seq_processing(self):
        seq2seq = Seq2SeqModel(seq2seq_model, seq2seq_tokenizer, 25)
        answer = seq2seq.get_answer(self.__question)
        self.__answer = answer
        self.__seq2seq = True
        if self.__voice:
            text_to_speech(answer)

    def __process_answer_with_add_info(self, data):
        self.__answer = str(data[0] + ' ' + data[1])
        if self.__voice:
            text_to_speech(data[0])
        self.__seq2seq = False

    def __process_answer(self, data):
        self.__answer = data[0]
        # self.__extract_info()
        if self.__struct_info != '':
            if self.__entity['type'] == self.__intent.split('_')[0]:
                self.__answer = self.__answer.replace('*', self.__struct_info)
                if self.__voice:
                    text_to_speech(self.__answer)
                self.__answer += ' ' + self.__process_struct_info()
            else:
                self.__answer = random.choice(ANSWERS_FOR_UNRECOGNIZED_QUESTIONS)
                if self.__voice:
                    text_to_speech(data[0])

    def __intent_processing(self):
        data = get_answer_from_tag(self.__intent)
        self.__options_for_questions = data[2]
        self.__additional_response = data[3]
        self.__seq2seq = False
        if data[1] != '':
            self.__process_answer_with_add_info(data)
        else:
            self.__process_answer(data)
            if self.__struct_info == '' and '*' in data[0]:
                self.__answer = 'Я не понял твой вопрос'

            if self.__voice:
                text_to_speech(self.__answer)

    def __process_good_response(self):
        self.__answer = random.choice(ANSWERS_FOR_GOOD_RESPONSE)
        if self.__voice:
            text_to_speech(self.__answer)

    def __process_greeting(self):
        hour = datetime.now().time().hour
        if 6 <= hour < 12:
            self.__answer = 'Доброе утро'
        elif 12 <= hour < 18:
            self.__answer = 'Добрый день'
        elif 18 <= hour < 24:
            self.__answer = 'Добрый вечер'
        elif 0 < hour < 6:
            self.__answer = 'Доброй ночи'

    def greeting(self):
        self.__process_greeting()
        self.__answer += '! ' + random.choice(GREETING_RESPONSE)
        if self.__voice:
            text_to_speech(self.__answer)

    def user_greeting(self, data):
        user_type = data['userType']
        access_token = data['accessToken']
        self.__process_greeting()
        user_name = get_user_name(user_type, access_token)
        self.__answer += ', ' + user_name + '! ' + random.choice(GREETING_RESPONSE)
        if self.__voice:
            text_to_speech(self.__answer)

    def get_response_user_auth(self, data):
        user_type = data['userType']
        access_token = data['accessToken']
        user_name = get_user_name(user_type, access_token)
        self.__answer += random.choice(LOGIN_USER_RESPONSE).replace('*', user_name)
        if self.__voice:
            text_to_speech(self.__answer)

    def get_response_user_logout(self):
        self.__answer += random.choice(LOGOUT_USER_RESPONSE)
        if self.__voice:
            text_to_speech(self.__answer)

    def get_response(self):
        return {
            "audioAnswer": self.__url_audio,
            "answer": self.__answer,
            "model": 'Seq2seqModel' if self.__seq2seq else 'IntentClassifierModel',
            "language": self.__language,
            "intent": self.__intent,
            "entity": self.__entity,
            "dataTime": datetime.now(),
            "accuracy": round(float(self.__intent_accuracy), 3),
            "optionalQuestions": self.__options_for_questions,
            "additionalResponse": self.__additional_response,
            "version": "1.0.5"
        }
