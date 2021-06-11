import random

from constants.constants import ANSWERS_FOR_UNAUTHORIZED
from functions.user import *


def default_response(response, user_type, user_token):
    return ''


def process_my_name(response, user_type, user_token):
    if user_token != '':
        name = get_user_name(user_type, user_token)
        return response.replace('*', name)
    return random.choice(ANSWERS_FOR_UNAUTHORIZED)


def process_my_department(response, user_type, user_token):
    if user_token != '':
        name = get_user_department(user_type, user_token)
        return response.replace('*', name)
    return random.choice(ANSWERS_FOR_UNAUTHORIZED)


def process_my_curriculum(response, user_type, user_token):
    if user_token != '':
        return response
    return random.choice(ANSWERS_FOR_UNAUTHORIZED)


user_intent = {
    'my_name': process_my_name,
    'my_department': process_my_department,
    'my_curriculum': process_my_curriculum
}
