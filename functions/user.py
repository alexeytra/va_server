import requests
from requests.exceptions import HTTPError
from constants.constants import ESSTU_URL


def get_user_name(user_type, user_token):
    try:
        if user_type == 'STUDENT':
            response = requests.get(ESSTU_URL + 'student/getInfo',
                                    headers={'Authorization': 'Bearer ' + user_token})
        else:
            response = requests.get(ESSTU_URL + 'employee/getInfo',
                                    headers={'Authorization': 'Bearer' + user_token})
        response.raise_for_status()
        return response.json()['firstName'] + ' ' + response.json()['patronymic']
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def get_user_department(user_type, user_token):
    try:
        if user_type == 'STUDENT':
            response = requests.get(ESSTU_URL + 'student/getInfo',
                                    headers={'Authorization': 'Bearer ' + user_token})
        else:
            response = requests.get(ESSTU_URL + 'employee/getInfo',
                                    headers={'Authorization': 'Bearer' + user_token})
        response.raise_for_status()
        return response.json()['chairName']
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')