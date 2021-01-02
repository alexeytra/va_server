import requests
import speech_recognition as sr


def text_to_speech(text):
    text = text.replace(" ", "%20")
    url = "https://tts.voicetech.yandex.net/generate?key=22fe10e2-aa2f-4a58-a934-54f2c1c4d908&" \
          "text=" + text + \
          "&format=mp3&lang=ru-RU&speed=1.0&emotion=neutral&speaker=kostya&robot=1"
    r = requests.get(url)
    with open('./temp_data/outputAudio.mp3', 'wb') as f:
        f.write(r.content)


def speech_to_text(audio):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio) as source:
            audio_data = r.record(source)
            command = r.recognize_google(audio_data, language='ru')
            return command

    except sr.UnknownValueError:
        return False

