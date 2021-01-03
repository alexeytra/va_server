import random
import json


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
    responses = ''
    add_info = ''
    for tg in load_intents()["intents"]:
        if tg['tag'] == tag:
            responses = tg['response']
            add_info = tg['add_info']
    response = random.choice(responses)
    return response, add_info
