BASE_URL = '/va/api/v1/'
KEY_WORDS = ['Системы информатики', 'СИ',
             'Электротехнический', 'ЭТФ',
             'Строительный', 'СФ', 'Электронно-вычислительные системы',
             'Электронно вычислительные системы', "ЭВС"]

ANSWERS_FOR_UNRECOGNIZED_QUESTIONS = ['Я не понял твой вопрос... 😔', 'Вы что-то сказали? 😁',
                                      'Это вы на каком языке сказали? 🧐',
                                      'Я вас не понимаю 🤪', 'Простите, что? 🤓',
                                      'Я не понял, что вы сказали! Можете повторить? 🐔']

DEPARTMENTS = {
    'системы информатики': 'kaf_si',
    'СИ': 'kaf_si',
    'Электронно-вычислительные системы': 'kaf_evs',
    'Электронно вычислительные системы': 'kaf_evs',
    'ЭВС': 'kaf_evs',
    'Тепловые электрические станции': 'kaf_tes',
    'ТЭС': 'kaf_tes',
    'Строительный': 'fac_sf',
    'строительного': 'fac_sf',
    'СФ': 'fac_sf'
}

CLASSROOMS = {
    '100': 'auditorium_aud100',
    '101': 'auditorium_aud101',
    '101а': 'auditorium_aud101a',
    '101б': 'auditorium_aud101б',
    '102': 'auditorium_aud102',
    '103': 'auditorium_aud103',
    '104': 'auditorium_aud104',
    '106': 'auditorium_aud106',
    '107': 'auditorium_aud107',
    '107a': 'auditorium_aud107a',
    '155': 'auditorium_aud155',
}

BUILDINGS = {
    'первый корпус': 'building_build1',
    'второй корпус': 'building_build2',
    'третий корпус': 'building_build3',
    'четвертый корпус': 'building_build4',
}