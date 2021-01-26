import random
import json

ANSWERS_FOR_UNRECOGNIZED_QUESTIONS = ['Я не понял твой вопрос... 😔', 'Вы что-то сказали? 😁',
                                      'Это вы на каком языке сказали? 🧐',
                                      'Я вас не понимаю 🤪', 'Простите, что? 🤓',
                                      'Я не понял, что вы сказали! Можете повторить? 🐔']


def load_intents():
    with open('./static/data/intents.json') as file:
        data = json.load(file)
    intents = {
        'pattern': [],
        'label': []
    }
    labels = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            intents['pattern'].append(pattern)
            intents['label'].append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])
    return data


def get_answer_from_tag(tag):
    response = ''
    add_info = ''
    if tag == 'unrecognized_question':
        response = random.choice(ANSWERS_FOR_UNRECOGNIZED_QUESTIONS)
        add_info = ''
    else:
        for tg in load_intents()["intents"]:
            if tg['tag'] == tag:
                response = tg['response']
                add_info = tg['add_info']
        response = random.choice(response)
    return response, add_info
