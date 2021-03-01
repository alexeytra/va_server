import random
import json

from utils.constants import ANSWERS_FOR_UNRECOGNIZED_QUESTIONS


def load_intents():
    with open('./static/data/intents.json', encoding='utf-8', mode='r') as file:
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


def load_additional_info(key, tag):
    tag = tag.split('_')[1]
    with open('./static/data/info_data.json', encoding='utf-8', mode='r') as file:
        data = json.load(file)
    return data[key][tag]
